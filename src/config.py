import os


# ============================================================
# SUPABASE
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


# ============================================================
# TELEGRAM
# ============================================================

TELEGRAM_BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN",
    ""
)

TELEGRAM_CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID",
    ""
)


# ============================================================
# GENERAL SETTINGS
# ============================================================

MAX_EVENTS_PER_RUN = int(
    os.getenv(
        "MAX_EVENTS_PER_RUN",
        "20"
    )
)


LOOKBACK_HOURS = int(
    os.getenv(
        "LOOKBACK_HOURS",
        "48"
    )
)


# ============================================================
# LOCATION KEYWORDS
# ============================================================

CHENNAI_KEYWORDS = [

    "chennai",
    "madras",

    "guindy",
    "adyar",
    "tambaram",
    "velachery",

    "porur",
    "perungudi",
    "sholinganallur",
    "sholinganallur",

    "omr",
    "ecr",

    "anna nagar",
    "t nagar",

    "nungambakkam",
    "egmore",

    "kelambakkam",
    "siruseri",

    "sriperumbudur",

    "chromepet",
    "pallavaram",

    "ambattur",

    "tharamani",

    "royapettah",

    "mount road"
]


# ============================================================
# EVENT KEYWORDS
# ============================================================

EVENT_KEYWORDS = [

    # Hackathons
    "hackathon",
    "hackfest",
    "hackathon 2026",
    "coding hackathon",

    # Coding
    "coding contest",
    "coding competition",
    "programming contest",

    # Developer
    "developer meetup",
    "developer meet",
    "developers meetup",
    "tech meetup",
    "developer conference",

    # Symposium
    "symposium",
    "technical symposium",
    "tech symposium",

    # Workshops
    "workshop",
    "technical workshop",
    "tech workshop",
    "hands on workshop",

    # Seminars
    "seminar",
    "technical seminar",

    # Conferences
    "conference",
    "tech conference",
    "technology conference",

    # AI
    "ai event",
    "ai workshop",
    "artificial intelligence workshop",
    "machine learning workshop",
    "machine learning meetup",
    "generative ai",

    # Cloud
    "cloud meetup",
    "cloud workshop",
    "aws meetup",
    "azure meetup",
    "google cloud meetup",

    # DevOps
    "devops meetup",
    "devops workshop",

    # Cybersecurity
    "cybersecurity event",
    "cyber security workshop",
    "cybersecurity workshop",

    # Data
    "data science meetup",
    "data science workshop",

    # Web
    "web development workshop",
    "web development meetup",

    # College
    "technical fest",
    "tech fest",
    "technical event",

    # Innovation
    "ideathon",
    "innovation challenge",
    "startup event",
    "innovation event"
]


# ============================================================
# SOURCE SEARCH QUERIES
# ============================================================

SEARCH_QUERIES = [

    '"Chennai" hackathon',

    '"Chennai" hackathon registration',

    '"Chennai" coding competition',

    '"Chennai" developer meetup',

    '"Chennai" tech meetup',

    '"Chennai" symposium',

    '"Chennai" technical symposium',

    '"Chennai" workshop technology',

    '"Chennai" AI workshop',

    '"Chennai" machine learning workshop',

    '"Chennai" developer conference',

    '"Chennai" technology conference',

    '"Chennai" cybersecurity workshop',

    '"Chennai" cloud workshop',

    '"Chennai" DevOps meetup',

    '"Chennai" technical fest',

    '"Chennai" ideathon',

    '"Chennai" innovation challenge'
]