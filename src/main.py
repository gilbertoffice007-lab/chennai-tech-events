import logging
import sys

from .sources import (
    fetch_all_sources
)

from .extractor import (
    parse_event
)

from .poster import (
    process_poster
)

from .deduplicator import (
    process_event
)

from .notifier import (
    format_caption,
    send_photo,
    send_text
)

from .event_database import (
    mark_notification_sent
)

from .config import (
    MAX_EVENTS_PER_RUN
)

# Ensure UTF-8 console output on Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass  # Older Python or non-Windows — encoding is usually fine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print(
        "=========================================="
    )
    print(
        "     CHENNAI TECH EVENTS SCANNER"
    )
    print(
        "=========================================="
    )
    print()


    # ========================================================
    # STEP 1 — COLLECT ARTICLES
    # ========================================================

    raw_articles = (
        fetch_all_sources()
    )


    print()
    print(
        f"Articles collected: "
        f"{len(raw_articles)}"
    )


    # ========================================================
    # TRACK PROCESSED EVENTS
    # ========================================================

    processed_event_ids = set()

    sent_count = 0

    update_count = 0


    # ========================================================
    # STEP 2 — PROCESS ARTICLES
    # ========================================================

    for article in raw_articles:

        if (
            sent_count
            >= MAX_EVENTS_PER_RUN
        ):

            break


        # ----------------------------------------------------
        # Convert article → event
        # ----------------------------------------------------

        event = parse_event(
            article
        )


        if event is None:

            continue


        # ----------------------------------------------------
        # Prevent duplicate articles
        # ----------------------------------------------------

        event_id = event[
            "event_id"
        ]


        if event_id in processed_event_ids:

            continue


        processed_event_ids.add(
            event_id
        )


        print()
        print(
            f"Processing: "
            f"{event['title']}"
        )


        # ====================================================
        # STEP 3 — POSTER
        # ====================================================

        poster_url = (
            process_poster(

                event[
                    "source_url"
                ],

                event_id
            )
        )


        if poster_url:

            event[
                "poster_url"
            ] = poster_url


            # Recalculate content hash
            from .extractor import (
                create_content_hash
            )

            event[
                "content_hash"
            ] = create_content_hash(
                event
            )


        # ====================================================
        # STEP 4 — DATABASE / DEDUPLICATION
        # ====================================================

        result = process_event(
            event
        )


        status = result[
            "status"
        ]


        # ====================================================
        # IGNORE
        # ====================================================

        if status == "IGNORE":

            print(
                "→ Already seen. "
                "Ignoring."
            )

            continue


        # ====================================================
        # NEW / UPDATE
        # ====================================================

        print(
            f"→ {status}"
        )


        # ----------------------------------------------------
        # Telegram caption
        # ----------------------------------------------------

        caption = format_caption(
            event,
            status
        )


        # ====================================================
        # SEND POSTER
        # ====================================================

        if poster_url:

            success = send_photo(

                poster_url,

                caption,

                event.get(
                    "registration_url"
                ),

                event.get(
                    "source_url"
                )
            )

        else:

            success = send_text(

                caption,

                event.get(
                    "registration_url"
                ),

                event.get(
                    "source_url"
                )
            )


        # ====================================================
        # MARK SENT
        # ====================================================

        if success:

            mark_notification_sent(
                event_id
            )

            sent_count += 1


            if status == "UPDATE":

                update_count += 1


            print(
                "✓ Telegram notification sent"
            )

        else:

            print(
                "✗ Telegram notification failed"
            )


    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print(
        "=========================================="
    )

    print(
        f"Notifications sent: "
        f"{sent_count}"
    )

    print(
        f"Updates: "
        f"{update_count}"
    )

    print(
        "=========================================="
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()