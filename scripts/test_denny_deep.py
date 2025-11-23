import requests
from bs4 import BeautifulSoup
import json
import re

print("Deep analysis of dulceriasdenny.com...\n")

url = "https://dulceriasdenny.com/productos"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    r = requests.get(url, headers=headers, timeout=10)
    
    if r.status_code == 200:
        # Look for API endpoints in source
        api_patterns = [
            r'https?://[^"\']+/api/[^"\']+',
            r'/api/[^"\']+',
            r'apiUrl["\']?\s*:\s*["\']([^"\']+)',
            r'endpoint["\']?\s*:\s*["\']([^"\']+)'
        ]
        
        found_apis = set()
        for pattern in api_patterns:
            matches = re.findall(pattern, r.text)
            found_apis.update(matches)
        
        if found_apis:
            print("Found API endpoints:")
            for api in list(found_apis)[:10]:
                print(f"  {api}")
        
        # Look for data in script tags
        soup = BeautifulSoup(r.text, 'html.parser')
        scripts = soup.find_all('script')
        
        print(f"\nAnalyzing {len(scripts)} script tags...")
        
        for script in scripts:
            script_text = script.string if script.string else ''
            
            # Look for product data
            if 'producto' in script_text.lower() or 'product' in script_text.lower():
                if 'precio' in script_text.lower() or 'price' in script_text.lower():
                    print("\nFound script with product and price data:")
                    print(script_text[:500])
                    break
        
        # Try to find the actual product container
        product_containers = soup.find_all(['div', 'article'], class_=lambda x: x and any(term in str(x).lower() for term in ['product', 'item', 'card']))
        print(f"\nFound {len(product_containers)} potential product containers")
        
        if product_containers:
            first = product_containers[0]
            print(f"\nFirst container classes: {first.get('class')}")
            print(f"First container HTML (first 300 chars):\n{str(first)[:300]}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
