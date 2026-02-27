import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_competitor_data(product_url):
    async with async_playwright() as p:
        # Launch browser in 'stealth' mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"🔍 Accessing: {product_url}")
        await page.goto(product_url)

        # Wait for reviews to load
        await page.wait_for_selector('.review-text-content')

        # 1. Extract Positive Reviews (Winning Features)
        positives = await page.locator('.review-rating[data-hook="review-star-rating"]:has-text("5.0 out of 5 stars")').all_inner_texts()
        
        # 2. Extract Negative Reviews (The "Gaps")
        negatives = await page.locator('.review-text-content:below(:text("1.0 out of 5 stars"))').all_inner_texts()

        data = {
            "source": product_url,
            "top_wins": positives[:5],
            "top_complaints": negatives[:10]
        }

        with open('market_gap.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        await browser.close()
        print("✅ Data saved to market_gap.json")

# Run it
asyncio.run(scrape_competitor_data("https://www.amazon.com/Amazon-Basics-Cancelling-Headphones-Bluetooth/dp/B0D46JP795/ref=sr_1_1_ffob_sspa?dib=eyJ2IjoiMSJ9.2QJaOaxqyyzZACh0Dbh27H-VFGsztVVMU425FIXtUE6ilEu2hZiD061NqeDcxjL-azemMQlbq51cf9K46EyiRqUzuku1GnbNwygM7ug92VC3s5TA6obkVLkfL7rZxKvo5roIci_Jxd7251bkE-Sz4n3InlJY3Xf34cJYsGsP27zQHsflVNAsZfRzkT3VqRugcZVu_crQIvi_M1-pAL3pwQ5W2E0lkiTbMz99d6xnqVI.7hsHnWKD_DesIdQGEGjDwNwmYrf8ZtkKrw5xu7lQE8k&dib_tag=se&keywords=Noise+Canceling+Headphones&qid=1772161804&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"))