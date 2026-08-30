import requests

from .config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)


# ============================================================
# TELEGRAM API
# ============================================================

TELEGRAM_API = (
    "https://api.telegram.org/"
    f"bot{TELEGRAM_BOT_TOKEN}"
)


# ============================================================
# FORMAT CAPTION
# ============================================================

def format_caption(
    event,
    status
):

    if status == "NEW":

        header = (
            "🚨 NEW CHENNAI TECH EVENT"
        )

    else:

        header = (
            "🔔 CHENNAI TECH EVENT UPDATE"
        )


    title = event.get(
        "title",
        "Unknown Event"
    )

    category = event.get(
        "category",
        "Technology"
    )

    organizer = event.get(
        "organizer"
    ) or "Not specified"

    location = event.get(
        "location"
    ) or "Chennai"

    event_date = event.get(
        "event_date"
    ) or "Not specified"

    deadline = event.get(
        "registration_deadline"
    ) or "Not specified"

    published = event.get(
        "published_date"
    ) or "Not specified"

    description = event.get(
        "description"
    ) or "No description available."


    # Telegram caption has length limits,
    # so keep description reasonable.

    description = description[:700]


    caption = f"""
{header}

💻 {title}

🏷️ Category:
{category}

🏢 Organizer:
{organizer}

📍 Location:
{location}

📢 Published:
{published}

📅 Event Date:
{event_date}

⏳ Registration Deadline:
{deadline}

📝 Description:
{description}
""".strip()


    return caption


# ============================================================
# SEND PHOTO
# ============================================================

def send_photo(
    poster_url,
    caption,
    registration_url=None,
    source_url=None
):

    if not TELEGRAM_BOT_TOKEN:

        print(
            "Telegram token missing."
        )

        return False

    if not TELEGRAM_CHAT_ID:

        print(
            "Telegram chat ID missing."
        )

        return False


    url = (
        f"{TELEGRAM_API}/sendPhoto"
    )


    # --------------------------------------------------------
    # Inline buttons
    # --------------------------------------------------------

    buttons = []

    if registration_url:

        buttons.append([
            {
                "text":
                    "🔗 Register Now",

                "url":
                    registration_url
            }
        ])


    if source_url:

        buttons.append([
            {
                "text":
                    "📄 View Source",

                "url":
                    source_url
            }
        ])


    payload = {

        "chat_id":
            TELEGRAM_CHAT_ID,

        "photo":
            poster_url,

        "caption":
            caption,

        "parse_mode":
            "HTML"
    }


    if buttons:

        payload["reply_markup"] = {
            "inline_keyboard":
                buttons
        }


    try:

        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return True

    except Exception as error:

        print(
            f"Telegram error: {error}"
        )

        return False


# ============================================================
# SEND TEXT WHEN POSTER NOT AVAILABLE
# ============================================================

def send_text(
    caption,
    registration_url=None,
    source_url=None
):

    if not TELEGRAM_BOT_TOKEN:

        return False

    if not TELEGRAM_CHAT_ID:

        return False


    url = (
        f"{TELEGRAM_API}/sendMessage"
    )


    buttons = []

    if registration_url:

        buttons.append([
            {
                "text":
                    "🔗 Register Now",

                "url":
                    registration_url
            }
        ])


    if source_url:

        buttons.append([
            {
                "text":
                    "📄 View Source",

                "url":
                    source_url
            }
        ])


    payload = {

        "chat_id":
            TELEGRAM_CHAT_ID,

        "text":
            caption,

        "parse_mode":
            "HTML"
    }


    if buttons:

        payload["reply_markup"] = {
            "inline_keyboard":
                buttons
        }


    try:

        response = requests.post(
            url,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return True

    except Exception as error:

        print(
            f"Telegram error: {error}"
        )

        return False