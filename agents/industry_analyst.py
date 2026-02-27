import re
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

async def find_industry_urls(industry_query):
    # 1. CamelCase to Spaces: 'BoxingGloves' -> 'Boxing Gloves'
    spaced_query = re.sub(r'(?<!^)(?=[A-Z])', ' ', industry_query)
    print(f"🔎 Researching the market for: {spaced_query}")
    API_KEY = os.getenv("TAVILY_API_KEY")
    if not API_KEY:
        raise ValueError("❌ TAVILY_API_KEY not found in .env file")
    url = "https://api.tavily.com/search"
    
    # 2. Iterative Search Strategy
    # We use multiple variations to ensure we find exactly 5 unique products
    query_variations = [
        f"site:amazon.com best selling {spaced_query} products 2026",
        f"site:amazon.com top rated {spaced_query} reviews 2026",
        f"site:amazon.com {spaced_query} premium brands"
    ]
    
    found_urls = []
    
    for query in query_variations:
        if len(found_urls) >= 5:
            break
            
        payload = {
            "api_key": API_KEY,
            "query": query,
            "search_depth": "advanced",
            "max_results": 15,
            "include_domains": ["amazon.com"]
        }
        
        try:
            response = requests.post(url, json=payload)
            results = response.json().get("results", [])
            
            for res in results:
                link = res['url']
                # Only grab actual product pages (/dp/)
                if "/dp/" in link:
                    # Strip tracking parameters to ensure uniqueness
                    clean_link = link.split("/ref=")[0].split("?")[0].rstrip("/")
                    
                    if clean_link not in found_urls:
                        found_urls.append(clean_link)
                        if len(found_urls) == 5:
                            break
        except Exception as e:
            print(f"⚠️ Search variation failed: {e}")

    # 3. Final Selection
    top_urls = found_urls[:5]
    
    print(f"🎯 Found exactly {len(top_urls)} top-tier competitor products.")

    # Save to data folder
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    file_path = data_dir / "industry_urls.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(top_urls, f, indent=4, ensure_ascii=False)
        
    return top_urls