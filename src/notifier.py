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

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    if status == "NEW":

        header = (
            "🚨 NEW CHENNAI TECH EVENT"
        )

    else:

        header = (
            "🔔 CHENNAI TECH EVENT UPDATE"
        )


    # --------------------------------------------------------
    # Event information
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Clean values
    # --------------------------------------------------------

    title = str(title).strip()
    category = str(category).strip()
    organizer = str(organizer).strip()
    location = str(location).strip()
    event_date = str(event_date).strip()
    deadline = str(deadline).strip()
    published = str(published).strip()
    description = str(description).strip()


    # --------------------------------------------------------
    # Telegram photo caption has a limited length.
    # Keep it reasonably short.
    # --------------------------------------------------------

    description = description[:600]


    # --------------------------------------------------------
    # Create caption
    #
    # IMPORTANT:
    # We intentionally DO NOT use parse_mode="HTML".
    #
    # This prevents characters such as:
    # &, <, >
    #
    # inside scraped website content from causing
    # Telegram 400 Bad Request errors.
    # --------------------------------------------------------

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
# CREATE INLINE BUTTONS
# ============================================================

def create_buttons(
    registration_url=None,
    source_url=None
):

    buttons = []


    # --------------------------------------------------------
    # Registration button
    # --------------------------------------------------------

    if registration_url:

        registration_url = str(
            registration_url
        ).strip()

        if registration_url:

            buttons.append([
                {
                    "text": "🔗 Register Now",
                    "url": registration_url
                }
            ])


    # --------------------------------------------------------
    # Source button
    # --------------------------------------------------------

    if source_url:

        source_url = str(
            source_url
        ).strip()

        if source_url:

            buttons.append([
                {
                    "text": "📄 View Source",
                    "url": source_url
                }
            ])


    # --------------------------------------------------------
    # Return Telegram format
    # --------------------------------------------------------

    if not buttons:

        return None


    return {
        "inline_keyboard": buttons
    }


# ============================================================
# SEND PHOTO
# ============================================================

def send_photo(
    poster_url,
    caption,
    registration_url=None,
    source_url=None
):

    # --------------------------------------------------------
    # Check token
    # --------------------------------------------------------

    if not TELEGRAM_BOT_TOKEN:

        print(
            "❌ Telegram bot token missing."
        )

        return False


    # --------------------------------------------------------
    # Check chat ID
    # --------------------------------------------------------

    if not TELEGRAM_CHAT_ID:

        print(
            "❌ Telegram chat ID missing."
        )

        return False


    # --------------------------------------------------------
    # Check poster URL
    # --------------------------------------------------------

    if not poster_url:

        print(
            "❌ Poster URL missing."
        )

        return False


    poster_url = str(
        poster_url
    ).strip()


    # --------------------------------------------------------
    # Telegram sendPhoto endpoint
    # --------------------------------------------------------

    url = (
        f"{TELEGRAM_API}/sendPhoto"
    )


    # --------------------------------------------------------
    # Inline buttons
    # --------------------------------------------------------

    reply_markup = create_buttons(
        registration_url,
        source_url
    )


    # --------------------------------------------------------
    # Payload
    #
    # IMPORTANT:
    # No parse_mode.
    # --------------------------------------------------------

    payload = {

        "chat_id":
            TELEGRAM_CHAT_ID,

        "photo":
            poster_url,

        "caption":
            caption
    }


    # --------------------------------------------------------
    # Add buttons if available
    # --------------------------------------------------------

    if reply_markup:

        payload["reply_markup"] = (
            reply_markup
        )


    # --------------------------------------------------------
    # Send request
    # --------------------------------------------------------

    try:

        print(
            "📤 Sending poster to Telegram..."
        )

        print(
            f"Poster URL: {poster_url}"
        )

        print(
            f"Chat ID: {TELEGRAM_CHAT_ID}"
        )


        response = requests.post(
            url,
            json=payload,
            timeout=30
        )


        # ----------------------------------------------------
        # DEBUG INFORMATION
        # ----------------------------------------------------

        print(
            f"Telegram status: "
            f"{response.status_code}"
        )

        print(
            f"Telegram response: "
            f"{response.text}"
        )


        # ----------------------------------------------------
        # Check response
        # ----------------------------------------------------

        response.raise_for_status()


        print(
            "✅ Telegram photo sent successfully."
        )

        return True


    except requests.exceptions.RequestException as error:

        print(
            "❌ Telegram request failed."
        )

        # ----------------------------------------------------
        # Print Telegram's actual error
        # ----------------------------------------------------

        if error.response is not None:

            print(
                "Telegram HTTP status:",
                error.response.status_code
            )

            print(
                "Telegram error response:",
                error.response.text
            )


        else:

            print(
                "No response received from Telegram."
            )


        return False


    except Exception as error:

        print(
            f"❌ Telegram error: {error}"
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

    # --------------------------------------------------------
    # Check token
    # --------------------------------------------------------

    if not TELEGRAM_BOT_TOKEN:

        print(
            "❌ Telegram bot token missing."
        )

        return False


    # --------------------------------------------------------
    # Check chat ID
    # --------------------------------------------------------

    if not TELEGRAM_CHAT_ID:

        print(
            "❌ Telegram chat ID missing."
        )

        return False


    # --------------------------------------------------------
    # Telegram sendMessage endpoint
    # --------------------------------------------------------

    url = (
        f"{TELEGRAM_API}/sendMessage"
    )


    # --------------------------------------------------------
    # Inline buttons
    # --------------------------------------------------------

    reply_markup = create_buttons(
        registration_url,
        source_url
    )


    # --------------------------------------------------------
    # Payload
    #
    # IMPORTANT:
    # No HTML parse mode.
    # --------------------------------------------------------

    payload = {

        "chat_id":
            TELEGRAM_CHAT_ID,

        "text":
            caption
    }


    # --------------------------------------------------------
    # Add buttons
    # --------------------------------------------------------

    if reply_markup:

        payload["reply_markup"] = (
            reply_markup
        )


    # --------------------------------------------------------
    # Send request
    # --------------------------------------------------------

    try:

        print(
            "📤 Sending text notification "
            "to Telegram..."
        )


        response = requests.post(
            url,
            json=payload,
            timeout=30
        )


        # ----------------------------------------------------
        # DEBUG INFORMATION
        # ----------------------------------------------------

        print(
            f"Telegram status: "
            f"{response.status_code}"
        )

        print(
            f"Telegram response: "
            f"{response.text}"
        )


        # ----------------------------------------------------
        # Check response
        # ----------------------------------------------------

        response.raise_for_status()


        print(
            "✅ Telegram text sent successfully."
        )

        return True


    except requests.exceptions.RequestException as error:

        print(
            "❌ Telegram request failed."
        )


        if error.response is not None:

            print(
                "Telegram HTTP status:",
                error.response.status_code
            )

            print(
                "Telegram error response:",
                error.response.text
            )


        else:

            print(
                "No response received from Telegram."
            )


        return False


    except Exception as error:

        print(
            f"❌ Telegram error: {error}"
        )

        return False
