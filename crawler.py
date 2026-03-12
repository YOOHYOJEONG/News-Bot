import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

SECTION_CONFIG = {
    "금융": {
        "url": "https://news.naver.com/breakingnews/section/101/259",
        "selectors": [
            ".section_latest .sa_text_title",
            "a.sa_text_title",
        ],
    },
    "부동산": {
        "url": "https://news.naver.com/breakingnews/section/101/260",
        "selectors": [
            ".section_latest .sa_text_title",
            "a.sa_text_title",
        ],
    },
    "경제": {
        "url": "https://news.naver.com/breakingnews/section/101/262",
        "selectors": [
            ".section_latest .sa_text_title",
            "a.sa_text_title",
        ],
    },
    "정치": {
        "url": "https://news.naver.com/section/100",
        "selectors": [
            ".section_component.as_section_headline .sa_text_title",
            ".section_article.as_headline .sa_text_title",
        ],
    },
    "사회": {
        "url": "https://news.naver.com/section/102",
        "selectors": [
            ".section_component.as_section_headline .sa_text_title",
            ".section_article.as_headline .sa_text_title",
        ],
    },
    "IT/과학": {
        "url": "https://news.naver.com/section/105",
        "selectors": [
            ".section_component.as_section_headline .sa_text_title",
            ".section_article.as_headline .sa_text_title",
        ],
    },
    "세계": {
        "url": "https://news.naver.com/section/104",
        "selectors": [
            ".section_component.as_section_headline .sa_text_title",
            ".section_article.as_headline .sa_text_title",
        ],
    },
}

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _extract_articles(soup: BeautifulSoup, selectors: list[str], base_url: str) -> list[dict[str, str]]:
    seen_links: set[str] = set()

    for selector in selectors:
        nodes = soup.select(selector)
        articles: list[dict[str, str]] = []

        for node in nodes:
            href = node.get("href")
            if not isinstance(href, str):
                continue

            link = urljoin(base_url, href)
            title = _normalize_text(node.get_text(" ", strip=True))
            if not title or link in seen_links:
                continue

            articles.append({"title": title, "link": link})
            seen_links.add(link)

            if len(articles) == 5:
                return articles

        if articles:
            return articles[:5]

    return []


def crawl_section(name: str, config: dict[str, object]) -> list[dict[str, str]]:
    url = config["url"]
    selectors = config["selectors"]

    response = requests.get(url, headers=REQUEST_HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = _extract_articles(soup, selectors, url)
    logger.info("Fetched %s articles from %s", len(articles), name)
    return articles


def crawl_all_news() -> dict[str, list[dict[str, str]]]:
    results: dict[str, list[dict[str, str]]] = {}

    for name, config in SECTION_CONFIG.items():
        try:
            results[name] = crawl_section(name, config)
        except requests.RequestException:
            logger.exception("Failed to fetch Naver section: %s", name)
            results[name] = []
        except Exception:
            logger.exception("Failed to parse Naver section: %s", name)
            results[name] = []

    return results
