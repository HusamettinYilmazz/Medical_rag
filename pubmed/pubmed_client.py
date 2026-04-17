import requests
import time

from utils.config import get_settings
settings = get_settings()


def search(term: str, retmax: int = 5) -> list[str]:
    url = settings.PUBMED_BASE_URL + "esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": term,
        "retmax": retmax,
        "sort": "date",
        "retmode": "json",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    pmids = data["esearchresult"]["idlist"]

    time.sleep(settings.REQUEST_DELAY)  # rate limit
    return pmids

def fetch(pmids: list[str]) -> str:
    if not pmids:
        return ""

    url = settings.PUBMED_BASE_URL + "efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    time.sleep(settings.REQUEST_DELAY)  # rate limit
    return response.text
