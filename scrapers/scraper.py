import asyncio
from playwright.async_api import async_playwright
import json
import os

async def scrape_product_reviews(page, product_url):
    """Helper function to scrape reviews for a single URL"""
    print(f"🔍 Scraping all reviews from: {product_url}")
    try:
        # Navigate and wait for content
        await page.goto(product_url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector('[data-hook="review-body"]', timeout=15000)

        # Extraction logic
        review_elements = await page.locator('[data-hook="review-body"] >> span').all_inner_texts()
        all_reviews = [text.strip() for text in review_elements if len(text.strip()) > 20]
        
        return {
            "source": product_url,
            "review_count": len(all_reviews),
            "raw_reviews": all_reviews
        }
    except Exception as e:
        print(f"⚠️ Failed to scrape {product_url}: {e}")
        return None

async def run_batch_scrape():
    # 1. Load the industry intelligence data
    data_path = 'data/industry_intelligence.json'
    
    if not os.path.exists(data_path):
        print(f"❌ Error: {data_path} not found. Run the analyst first.")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        competitor_list = json.load(f) # competitor_list is now your array of objects/URLs

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        final_results = []

        # 2. Iterate over the URLs found by the industry analyst
        # Assuming industry_analyst saved a list of dictionaries with a 'url' key
        for entry in competitor_list:
            url = entry if isinstance(entry, str) else entry.get('url')
            if url:
                result = await scrape_product_reviews(page, url)
                if result:
                    final_results.append(result)
                
                # Ethical/Anti-Bot delay
                await asyncio.sleep(2)

        # 3. Save the final deep-dive data
        with open('data/raw_reviews.json', 'w', encoding='utf-8') as f:
            json.dump(final_results, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Successfully processed {len(final_results)} products. Data saved.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_batch_scrape())