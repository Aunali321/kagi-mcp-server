import json
import os
from fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP(
    name="Kagi Search",
    instructions="""
        This server provides Kagi search capabilities.
        First call authenticate() with your Kagi token to save cookies.
        Then use search() to perform searches using your authenticated session.
    """,
)-

COOKIES_FILE = "kagi_cookies.json"


@mcp.tool
async def authenticate(token: str) -> str:
    """
    Authenticate with Kagi and save cookies for future searches.

    Args:
        token: Your Kagi authentication token from the URL

    Returns:
        Success or error message
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(f"https://kagi.com/search?token={token}")
        cookies = await context.cookies()

        with open(COOKIES_FILE, "w") as f:
            json.dump(cookies, f)

        await browser.close()
        return "Successfully authenticated! Cookies saved."


@mcp.tool
async def search(query: str, max_results: int = 10) -> list[dict]:
    """
    Search Kagi using saved authentication cookies.

    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 10)

    Returns:
        List of search results with rank, title, url, and snippet
    """
    if not os.path.exists(COOKIES_FILE):
        raise ValueError(
            f"Not authenticated! Cookie file '{COOKIES_FILE}' not found. "
            "Please run authenticate() with your Kagi token first."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Load cookies
        with open(COOKIES_FILE) as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(f"https://kagi.com/search?q={query}")
        await page.wait_for_selector(".search-result", timeout=5000)

        results = await page.query_selector_all(".search-result")

        output_data = []

        for i, result in enumerate(results[:max_results], 1):
            title_elem = await result.query_selector(".__sri-title")
            url_elem = await result.query_selector(".__sri-url-box a")
            snippet_elem = await result.query_selector(".__sri-desc")

            if title_elem and url_elem:
                title = await title_elem.inner_text()
                url = await url_elem.get_attribute("href")
                snippet = await snippet_elem.inner_text() if snippet_elem else ""

                output_data.append({
                    "rank": i,
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                })

        await browser.close()
        return output_data


if __name__ == "__main__":
    mcp.run()
