import logging

import requests

from bs4 import BeautifulSoup

from .supabase_client import supabase

logger = logging.getLogger(__name__)

BUCKET_NAME = "event-posters"


# ============================================================
# DOWNLOAD IMAGE
# ============================================================

def download_image(url):

    if not url:

        return None

    try:

        headers = {

            "User-Agent":
                "Mozilla/5.0 "
                "(compatible; "
                "ChennaiTechEventsBot/1.0)"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if "image" not in content_type:

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

def find_poster_from_page(
    page_url
):

    if not page_url:

        return None

    try:

        headers = {

            "User-Agent":
                "Mozilla/5.0 "
                "(compatible; "
                "ChennaiTechEventsBot/1.0)"
        }

        response = requests.get(
            page_url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # First try OpenGraph image
        og_image = soup.find(
            "meta",
            property="og:image"
        )

        if og_image:

            image_url = og_image.get(
                "content"
            )

            if image_url:

                return image_url


        # Then try Twitter image
        twitter_image = soup.find(
            "meta",
            attrs={
                "name":
                    "twitter:image"
            }
        )

        if twitter_image:

            image_url = twitter_image.get(
                "content"
            )

            if image_url:

                return image_url


        # Finally inspect images
        for image in soup.find_all(
            "img"
        ):

            src = image.get(
                "src"
            )

            if src and (
                ".jpg" in src.lower()
                or
                ".jpeg" in src.lower()
                or
                ".png" in src.lower()
                or
                ".webp" in src.lower()
            ):

                return src

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

    if not image_bytes:

        return None

    filename = (
        f"{event_id}.jpg"
    )

    try:

        # Remove existing file if any
        try:

            supabase.storage \
                .from_(BUCKET_NAME) \
                .remove([
                    filename
                ])

        except Exception:

            pass


        supabase.storage \
            .from_(BUCKET_NAME) \
            .upload(
                filename,
                image_bytes,
                {
                    "content-type":
                        "image/jpeg",
                    "upsert":
                        "true"
                }
            )


        public_url = (
            supabase.storage
            .from_(BUCKET_NAME)
            .get_public_url(
                filename
            )
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

    image_url = (
        find_poster_from_page(
            source_url
        )
    )

    if not image_url:

        return None


    image_bytes = (
        download_image(
            image_url
        )
    )

    if not image_bytes:

        return None


    poster_url = upload_poster(
        image_bytes,
        event_id
    )

    return poster_url
