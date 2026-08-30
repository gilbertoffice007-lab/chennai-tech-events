import hashlib
import re

from bs4 import BeautifulSoup

from dateutil import parser

from .config import (
    CHENNAI_KEYWORDS
)


# ============================================================
# CLEAN HTML
# ============================================================

def clean_html(text):

    if not text:

        return ""

    soup = BeautifulSoup(
        text,
        "html.parser"
    )

    return soup.get_text(
        " ",
        strip=True
    )


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CHENNAI CHECK
# ============================================================

def contains_chennai(text):

    normalized = normalize(
        text
    )

    for keyword in CHENNAI_KEYWORDS:

        if keyword in normalized:

            return True

    return False


# ============================================================
# EVENT CHECK
# ============================================================

def detect_category(text):

    normalized = normalize(
        text
    )

    categories = {

        "Hackathon": [
            "hackathon",
            "hackfest"
        ],

        "Coding": [
            "coding contest",
            "coding competition",
            "programming contest"
        ],

        "Developer Meetup": [
            "developer meetup",
            "developer meet",
            "developers meetup"
        ],

        "Technology Meetup": [
            "tech meetup",
            "technology meetup"
        ],

        "Symposium": [
            "symposium",
            "technical symposium"
        ],

        "Workshop": [
            "workshop",
            "technical workshop",
            "tech workshop"
        ],

        "Conference": [
            "conference",
            "tech conference"
        ],

        "AI / ML": [
            "artificial intelligence",
            "machine learning",
            "ai workshop",
            "ai event",
            "generative ai"
        ],

        "Cloud": [
            "cloud workshop",
            "cloud meetup",
            "aws meetup",
            "azure meetup",
            "google cloud meetup"
        ],

        "DevOps": [
            "devops meetup",
            "devops workshop"
        ],

        "Cybersecurity": [
            "cybersecurity",
            "cyber security workshop"
        ],

        "Data Science": [
            "data science meetup",
            "data science workshop"
        ],

        "Technical Fest": [
            "technical fest",
            "tech fest"
        ],

        "Ideathon": [
            "ideathon",
            "innovation challenge"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in normalized:

                return category

    return None


# ============================================================
# DATE EXTRACTION
# ============================================================

def extract_dates(text):

    patterns = [

        # 25 September 2026
        r"\b\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|July|"
        r"August|September|October|November|December)"
        r"\s+\d{4}\b",

        # September 25, 2026
        r"\b(?:January|February|March|April|May|June|July|"
        r"August|September|October|November|December)"
        r"\s+\d{1,2},?\s+\d{4}\b",

        # 25/09/2026
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    ]

    matches = []

    for pattern in patterns:

        found = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        matches.extend(
            found
        )

    return matches


# ============================================================
# PUBLICATION DATE
# ============================================================

def normalize_published_date(value):

    if not value:

        return None

    try:

        date = parser.parse(
            value
        )

        return date.isoformat()

    except Exception:

        return None


# ============================================================
# EVENT ID
# ============================================================

def create_event_id(
    title,
    organizer,
    event_date
):

    identity = "|".join([

        normalize(title),

        normalize(
            organizer or ""
        ),

        normalize(
            event_date or ""
        )
    ])

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()[:32]


# ============================================================
# CONTENT HASH
# ============================================================

def create_content_hash(event):

    content = "|".join([

        normalize(
            event.get(
                "title",
                ""
            )
        ),

        normalize(
            event.get(
                "organizer",
                ""
            )
        ),

        normalize(
            event.get(
                "category",
                ""
            )
        ),

        normalize(
            event.get(
                "event_date",
                ""
            )
        ),

        normalize(
            event.get(
                "registration_deadline",
                ""
            )
        ),

        normalize(
            event.get(
                "registration_url",
                ""
            )
        ),

        normalize(
            event.get(
                "location",
                ""
            )
        ),

        normalize(
            event.get(
                "description",
                ""
            )
        ),

        normalize(
            event.get(
                "poster_url",
                ""
            )
        )
    ])

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


# ============================================================
# PARSE EVENT
# ============================================================

def parse_event(item):

    title = clean_html(
        item.get(
            "title",
            ""
        )
    )

    description = clean_html(
        item.get(
            "summary",
            ""
        )
    )

    combined_text = (
        f"{title} {description}"
    )

    # --------------------------------------------------------
    # CHENNAI FILTER
    # --------------------------------------------------------

    if not contains_chennai(
        combined_text
    ):

        return None


    # --------------------------------------------------------
    # EVENT CATEGORY
    # --------------------------------------------------------

    category = detect_category(
        combined_text
    )

    if not category:

        return None


    # --------------------------------------------------------
    # DATES
    # --------------------------------------------------------

    dates = extract_dates(
        combined_text
    )

    event_date = None

    registration_deadline = None

    if dates:

        event_date = dates[0]

    if len(dates) > 1:

        registration_deadline = dates[1]


    # --------------------------------------------------------
    # CREATE EVENT
    # --------------------------------------------------------

    event = {

        "title":
            title,

        "organizer":
            None,

        "category":
            category,

        "location":
            "Chennai",

        "event_date":
            event_date,

        "registration_deadline":
            registration_deadline,

        "registration_url":
            None,

        "source_url":
            item.get(
                "url",
                ""
            ),

        "poster_url":
            None,

        "description":
            description,

        "published_date":
            normalize_published_date(
                item.get(
                    "published",
                    ""
                )
            )
    }


    # --------------------------------------------------------
    # EVENT ID
    # --------------------------------------------------------

    event["event_id"] = create_event_id(

        event["title"],

        event["organizer"],

        event["event_date"]
    )


    # --------------------------------------------------------
    # CONTENT HASH
    # --------------------------------------------------------

    event["content_hash"] = (
        create_content_hash(
            event
        )
    )


    return event

import requests


def fetch_source_page(url):

    if not url:

        return ""

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
            timeout=15
        )

        response.raise_for_status()

        return response.text

    except Exception as error:

        print(
            f"Page fetch failed: {error}"
        )

        return ""


def extract_page_text(url):

    html = fetch_source_page(
        url
    )

    if not html:

        return ""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Remove unnecessary elements
    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):

        element.decompose()

    text = soup.get_text(
        " ",
        strip=True
    )

    return text[:10000]