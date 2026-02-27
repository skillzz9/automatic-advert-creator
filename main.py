import asyncio
import sys
import re
# Ensure your industry_analyst script is correctly imported
from agents.industry_analyst import find_industry_urls


async def main():
    # 1. Validation: Check if the user provided the niche name
    if len(sys.argv) < 2:
        print("❌ Usage: python main.py <NicheName>")
        print("Example: python main.py NoiseCancellingHeadphone")
        return

    # 2. Extract input
    niche = sys.argv[1]

    print(f"\n🚀 Initiating Industry Analysis for: {niche}")
    print("--------------------------------------------------")
    
    try:
        # 3. Trigger the Analyst (Wait for it to finish search & file writing)
        # You MUST use 'await' here because run_full_analysis is async
        await find_industry_urls(niche)

        print(f"\n✅ Success! Competitor URLs have been saved to 'data/industry_urls.json'.")
        print("💡 You can now run Phase 2 (The Scraper) to gather reviews.")
        
    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")

if __name__ == "__main__":
    # Start the event loop
    asyncio.run(main())