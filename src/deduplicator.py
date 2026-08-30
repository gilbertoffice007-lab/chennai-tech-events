from .event_database import (
    find_event,
    insert_event,
    update_event
)


# ============================================================
# PROCESS EVENT
# ============================================================

def process_event(event):

    existing = find_event(
        event["event_id"]
    )


    # ========================================================
    # NEW EVENT
    # ========================================================

    if existing is None:

        insert_event(
            event
        )

        return {
            "status":
                "NEW",

            "event":
                event
        }


    # ========================================================
    # EVENT EXISTS
    # ========================================================

    old_hash = existing.get(
        "content_hash"
    )

    new_hash = event.get(
        "content_hash"
    )


    # ========================================================
    # EVENT UPDATED
    # ========================================================

    if old_hash != new_hash:

        update_event(
            event
        )

        return {
            "status":
                "UPDATE",

            "event":
                event,

            "old":
                existing
        }


    # ========================================================
    # NOTHING CHANGED
    # ========================================================

    return {

        "status":
            "IGNORE",

        "event":
            event
    }