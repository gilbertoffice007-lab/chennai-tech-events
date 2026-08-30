import feedparser

from urllib.parse import quote

from .config import SEARCH_QUERIES


# ============================================================
# GOOGLE NEWS RSS
# ============================================================

def build_google_news_url(query):

    encoded_query = quote(query)

    return (
        "https://news.google.com/rss/search?"
        f"q={encoded_query}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )


# ============================================================
# FETCH ONE QUERY
# ============================================================

def fetch_query(query):

    url = build_google_news_url(
        query
    )

    print(
        f"Searching: {query}"
    )

    try:

        feed = feedparser.parse(
            url
        )

        results = []

        for entry in feed.entries:

            results.append({

                "title":
                    entry.get(
                        "title",
                        ""
                    ),

                "url":
                    entry.get(
                        "link",
                        ""
                    ),

                "published":
                    entry.get(
                        "published",
                        ""
                    ),

                "summary":
                    entry.get(
                        "summary",
                        ""
                    ),

                "source":
                    "Google News"
            })

        return results

    except Exception as error:

        print(
            f"Search error: {error}"
        )

        return []


# ============================================================
# FETCH ALL
# ============================================================

def fetch_all_sources():

    all_results = []

    seen_urls = set()

    for query in SEARCH_QUERIES:

        results = fetch_query(
            query
        )

        for item in results:

            url = item.get(
                "url",
                ""
            )

            if not url:

                continue

            if url in seen_urls:

                continue

            seen_urls.add(url)

            all_results.append(
                item
            )

    print(
        f"Total unique articles: "
        f"{len(all_results)}"
    )

    return all_results