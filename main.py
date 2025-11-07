from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/search")
def search(q: str = Query(..., description="Search query")):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com", wait_until="domcontentloaded")
        page.fill("input[name=q]", q)
        page.keyboard.press("Enter")
        page.wait_for_selector("h3")
        results = []
        for el in page.query_selector_all("h3")[:5]:
            title = el.inner_text()
            parent = el.closest("a")
            href = parent.get_attribute("href") if parent else ""
            results.append({"title": title, "url": href})
        browser.close()
        return {"query": q, "results": results}
