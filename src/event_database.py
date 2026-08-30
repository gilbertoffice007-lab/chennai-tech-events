import logging

from datetime import datetime, timezone

from .supabase_client import supabase

logger = logging.getLogger(__name__)


# ============================================================
# FIND EVENT
# ============================================================

def find_event(event_id):

    try:

        response = (
            supabase
            .table("events")
            .select("*")
            .eq(
                "event_id",
                event_id
            )
            .limit(1)
            .execute()
        )

    except Exception as error:

        logger.error(
            "Supabase find_event failed: %s",
            error
        )

        return None

    if response.data:

        return response.data[0]

    return None


# ============================================================
# INSERT EVENT
# ============================================================

def insert_event(event):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    data = {

        "event_id":
            event["event_id"],

        "title":
            event["title"],

        "organizer":
            event.get("organizer"),

        "category":
            event.get("category"),

        "location":
            event.get("location"),

        "event_date":
            event.get("event_date"),

        "registration_deadline":
            event.get(
                "registration_deadline"
            ),

        "registration_url":
            event.get(
                "registration_url"
            ),

        "source_url":
            event["source_url"],

        "poster_url":
            event.get("poster_url"),

        "description":
            event.get("description"),

        "published_date":
            event.get(
                "published_date"
            ),

        "first_seen":
            now,

        "last_seen":
            now,

        "content_hash":
            event["content_hash"],

        "notification_sent":
            False,

        "updated_at":
            now
    }

    try:

        response = (
            supabase
            .table("events")
            .insert(data)
            .execute()
        )

        return response.data

    except Exception as error:

        logger.error(
            "Supabase insert_event failed: %s",
            error
        )

        return None


# ============================================================
# UPDATE EVENT
# ============================================================

def update_event(event):

    now = datetime.now(
        timezone.utc
    ).isoformat()

    data = {

        "title":
            event["title"],

        "organizer":
            event.get("organizer"),

        "category":
            event.get("category"),

        "location":
            event.get("location"),

        "event_date":
            event.get("event_date"),

        "registration_deadline":
            event.get(
                "registration_deadline"
            ),

        "registration_url":
            event.get(
                "registration_url"
            ),

        "source_url":
            event["source_url"],

        "poster_url":
            event.get("poster_url"),

        "description":
            event.get("description"),

        "published_date":
            event.get(
                "published_date"
            ),

        "last_seen":
            now,

        "content_hash":
            event["content_hash"],

        "notification_sent":
            False,

        "updated_at":
            now
    }

    try:

        response = (
            supabase
            .table("events")
            .update(data)
            .eq(
                "event_id",
                event["event_id"]
            )
            .execute()
        )

        return response.data

    except Exception as error:

        logger.error(
            "Supabase update_event failed: %s",
            error
        )

        return None


# ============================================================
# MARK NOTIFICATION SENT
# ============================================================

def mark_notification_sent(event_id):

    try:

        (
            supabase
            .table("events")
            .update({
                "notification_sent": True
            })
            .eq(
                "event_id",
                event_id
            )
            .execute()
        )

    except Exception as error:

        logger.error(
            "Supabase mark_notification_sent failed: %s",
            error
        )
