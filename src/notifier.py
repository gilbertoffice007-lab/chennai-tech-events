import json
import logging

import requests

from .config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)

logger = logging.getLogger(__name__)

TELEGRAM_API = (
    f"https://api.telegram.org/bot"
    f"{TELEGRAM_BOT_TOKEN}"
)


# ============================================================
# FORMAT CAPTION
# ============================================================

def format_caption(
    event,
    status="NEW"
):
    """
    Create Telegram caption.
    """

    title = event.get(
        "title",
        "Untitled Event"
    )

    category = event.get(
        "category",
        "Technology Event"
    )

    organizer = event.get(
        "organizer",
        "Not specified"
    )

    location = event.get(
        "location",
        "Chennai"
    )

    published_at = event.get(
        "published_at",
        "Not specified"
    )

    event_date = event.get(
        "event_date",
        "Not specified"
    )

    deadline = event.get(
        "registration_deadline",
        "Not specified"
    )

    description = event.get(
        "description",
        ""
    )

    # --------------------------------------------------------
    # Limit description
    # --------------------------------------------------------

    if description:

        description = str(
            description
        ).strip()

        if len(description) > 700:

            description = (
                description[:700]
                + "..."
            )

    else:

        description = (
            "No description available."
        )

    caption = (
        f"🚀 {status}: {title}\n\n"

        f"📂 Category: {category}\n"
        f"🏢 Organizer: {organizer}\n"
        f"📍 Location: {location}\n\n"

        f"📰 Published: {published_at}\n"
        f"📅 Event Date: {event_date}\n"
        f"⏰ Registration Deadline: {deadline}\n\n"

        f"📝 Description:\n"
        f"{description}"
    )

    return caption


# ============================================================
# CREATE BUTTONS
# ============================================================

def create_buttons(
    registration_url=None,
    source_url=None
):

    buttons = []

    if registration_url:

        buttons.append([
            {
                "text": "📝 Register",
                "url": registration_url
            }
        ])

    if source_url:

        buttons.append([
            {
                "text": "📰 View Source",
                "url": source_url
            }
        ])

    if not buttons:

        return None

    return {
        "inline_keyboard": buttons
    }


# ============================================================
# SEND PHOTO
# ============================================================

def send_photo(
    image_bytes,
    caption,
    registration_url=None,
    source_url=None
):
    """
    Upload image directly to Telegram.

    IMPORTANT:
    We do NOT give Telegram a URL.
    """

    if not image_bytes:

        logger.error(
            "No image bytes provided."
        )

        return False

    if not TELEGRAM_BOT_TOKEN:

        logger.error(
            "TELEGRAM_BOT_TOKEN is missing."
        )

        return False

    if not TELEGRAM_CHAT_ID:

        logger.error(
            "TELEGRAM_CHAT_ID is missing."
        )

        return False

    try:

        url = (
            f"{TELEGRAM_API}/sendPhoto"
        )

        reply_markup = create_buttons(
            registration_url,
            source_url
        )

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": caption
        }

        if reply_markup:

            data["reply_markup"] = json.dumps(
                reply_markup
            )

        # ----------------------------------------------------
        # Upload image bytes directly
        # ----------------------------------------------------

        files = {
            "photo": (
                "poster.jpg",
                image_bytes,
                "image/jpeg"
            )
        }

        logger.info(
            "Uploading poster directly to Telegram..."
        )

        response = requests.post(
            url,
            data=data,
            files=files,
            timeout=60
        )

        logger.info(
            "Telegram status: %s",
            response.status_code
        )

        logger.info(
            "Telegram response: %s",
            response.text
        )

        if response.ok:

            return True

        logger.error(
            "Telegram photo request failed."
        )

        return False

    except Exception as error:

        logger.error(
            "Telegram photo error: %s",
            error
        )

        return False


# ============================================================
# SEND TEXT
# ============================================================

def send_text(
    caption,
    registration_url=None,
    source_url=None
):
    """
    Send text message when no poster exists.
    """

    if not TELEGRAM_BOT_TOKEN:

        logger.error(
            "TELEGRAM_BOT_TOKEN is missing."
        )

        return False

    if not TELEGRAM_CHAT_ID:

        logger.error(
            "TELEGRAM_CHAT_ID is missing."
        )

        return False

    try:

        url = (
            f"{TELEGRAM_API}/sendMessage"
        )

        reply_markup = create_buttons(
            registration_url,
            source_url
        )

        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": caption
        }

        if reply_markup:

            data["reply_markup"] = json.dumps(
                reply_markup
            )

        response = requests.post(
            url,
            data=data,
            timeout=30
        )

        logger.info(
            "Telegram status: %s",
            response.status_code
        )

        logger.info(
            "Telegram response: %s",
            response.text
        )

        if response.ok:

            return True

        logger.error(
            "Telegram text request failed."
        )

        return False

    except Exception as error:

        logger.error(
            "Telegram text error: %s",
            error
        )

        return False
