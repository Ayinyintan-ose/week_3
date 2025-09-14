import asyncio
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

# To fetch the content of a url
async def fetch_page(sessions, url):
    try:
        async with sessions.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Sorry couldn't fetch {url}: {e}")
        return None

# parse the HTML content and extract data
async def parse_page(html_content, url):
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string if soup.title else "Title not found."
        print(f"Scraped {title} from {url}")
        return {"url": url, "title": title}
    return {"url": url,"title": "Couldn't scrape"}

# Scrape multiple urls
async def scrape_urls_concurrently(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(fetch_and_parse(session, url)))
        results = await asyncio.gather(*tasks)
        return [res for res in results if res is not None]

# Combines fetching and parsing for a single url
async def fetch_and_parse(session, url):
    html_content = await fetch_page(session, url)
    if html_content:
        return await parse_page(html_content, url)
    return {"url": url, "title": "Couldn't scrape data"}

if __name__ == "__main__":
    target_urls = [
        "http://quotes.toscrape.com/",
        "http://quotes.toscrape.com/page/2/",
        "http://quotes.toscrape.com/page/3/",
        "https://www.example.com"
    ]

    print("Starting scraping.....")
    scraped_data = asyncio.run(scrape_urls_concurrently(target_urls))
    print("\nScraping complete. Results:")
    for item in scraped_data:
        print(item)