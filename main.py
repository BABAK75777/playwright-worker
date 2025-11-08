from fastapi import FastAPI, Query
import httpx
from urllib.parse import urlparse, parse_qs, unquote
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    url = "https://duckduckgo.com/html/"
    params = {"q": q}

    try:
        resp = httpx.get(
            url,
            params=params,
            timeout=15.0,
            follow_redirects=True,
        )
        resp.raise_for_status()
    except Exception as e:
        return {
            "query": q,
            "results": [],
            "error": str(e),
        }

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for a in soup.select("a.result__a")[:5]:
        title = a.get_text(strip=True)
        href = a.get("href")
        results.append({"title": title, "url": href})

    return {"query": q, "results": results}
