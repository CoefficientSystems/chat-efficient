"""Handy utils for the notebooks."""
import time

import bs4
import requests
from joblib import Memory

LOCATION = "./cachedir"
MEMORY = Memory(LOCATION, verbose=0)


@MEMORY.cache
def scrape_page(url, sleep=0.2):
    """Scrape plain text from URL."""
    if "http://" not in url and "https://" not in url:
        url = f"http://{url}"

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=300)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    text = soup.body.get_text(" ", strip=True)

    if sleep:
        time.sleep(sleep)

    return text
