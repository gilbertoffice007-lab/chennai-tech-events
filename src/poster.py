import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .supabase_client import supabase

logger = logging.getLogger(__name__)

BUCKET_NAME = "event-posters"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


# ============================================================
# DOWNLOAD IMAGE
# ============================================================

def download_image(url):
    """
    Download an image and return its bytes.
    """

    if not url:
        return None

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
            allow_redirects=True
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        logger.info(
            "Image download: %s | %s",
            response.status_code,
            content_type
        )

        if "image" not in content_type:
            logger.warning(
                "URL did not return an image: %s",
                url
            )
            return None

        return response.content

    except Exception as error:
        logger.error(
            "Image download failed: %s",
            error
        )
        return None


# ============================================================
# FIND IMAGE ON PAGE
# ============================================================

def find_poster_from_page(page_url):
    """
    Find the most likely poster/image URL from an article page.
    """

    if not page_url:
        return None

    try:
        response = requests.get(
            page_url,
            headers=HEADERS,
            timeout=30,
            allow_redirects=True
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ----------------------------------------------------
        # 1. OpenGraph image
        # ----------------------------------------------------

        og_image = soup.find(
            "meta",
            property="og:image"
        )

        if og_image:

            image_url = og_image.get("content")

            if image_url:

                image_url = urljoin(
                    response.url,
                    image_url
                )

                logger.info(
                    "Poster found using og:image: %s",
                    image_url
                )

                return image_url

        # ----------------------------------------------------
        # 2. Twitter image
        # ----------------------------------------------------

        twitter_image = soup.find(
            "meta",
            attrs={
                "name": "twitter:image"
            }
        )

        if twitter_image:

            image_url = twitter_image.get(
                "content"
            )

            if image_url:

                image_url = urljoin(
                    response.url,
                    image_url
                )

                logger.info(
                    "Poster found using twitter:image: %s",
                    image_url
                )

                return image_url

        # ----------------------------------------------------
        # 3. Article image
        # ----------------------------------------------------

        for image in soup.find_all("img"):

            src = image.get("src")

            if not src:
                continue

            image_url = urljoin(
                response.url,
                src
            )

            lower_url = image_url.lower()

            if any(
                extension in lower_url
                for extension in (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp"
                )
            ):

                logger.info(
                    "Poster found using img tag: %s",
                    image_url
                )

                return image_url

        logger.warning(
            "No poster found for: %s",
            page_url
        )

    except Exception as error:

        logger.error(
            "Poster discovery failed: %s",
            error
        )

    return None


# ============================================================
# UPLOAD TO SUPABASE
# ============================================================

def upload_poster(
    image_bytes,
    event_id
):
    """
    Upload poster to Supabase Storage.

    IMPORTANT:
    We do NOT delete the old file first.
    """

    if not image_bytes:
        return None

    filename = f"{event_id}.jpg"

    try:

        # ----------------------------------------------------
        # Upload / overwrite existing file
        # ----------------------------------------------------

        supabase.storage \
            .from_(BUCKET_NAME) \
            .upload(
                filename,
                image_bytes,
                {
                    "content-type": "image/jpeg",
                    "upsert": "true"
                }
            )

        # ----------------------------------------------------
        # Generate public URL
        # ----------------------------------------------------

        public_url = (
            supabase.storage
            .from_(BUCKET_NAME)
            .get_public_url(filename)
        )

        # Remove accidental trailing ?
        if public_url:
            public_url = public_url.rstrip("?")

        logger.info(
            "Poster uploaded successfully: %s",
            public_url
        )

        return public_url

    except Exception as error:

        logger.error(
            "Poster upload failed: %s",
            error
        )

        return None


# ============================================================
# COMPLETE POSTER PROCESS
# ============================================================

def process_poster(
    source_url,
    event_id
):
    """
    Download poster, upload to Supabase,
    and return both URL and image bytes.

    Returns:
        {
            "url": "...",
            "bytes": b"..."
        }

        or None
    """

    # --------------------------------------------------------
    # Find image
    # --------------------------------------------------------

    image_url = find_poster_from_page(
        source_url
    )

    if not image_url:

        logger.warning(
            "No poster URL found."
        )

        return None

    # --------------------------------------------------------
    # Download image
    # --------------------------------------------------------

    image_bytes = download_image(
        image_url
    )

    if not image_bytes:

        logger.warning(
            "Poster download failed."
        )

        return None

    # --------------------------------------------------------
    # Upload to Supabase
    # --------------------------------------------------------

    poster_url = upload_poster(
        image_bytes,
        event_id
    )

    if not poster_url:

        logger.warning(
            "Poster could not be uploaded."
        )

        return None

    # --------------------------------------------------------
    # Return BOTH
    # --------------------------------------------------------

    return {
        "url": poster_url,
        "bytes": image_bytes
    }
