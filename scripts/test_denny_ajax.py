import requests
import json

print("Testing potential AJAX endpoints for dulceriasdenny.com...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}

# Common API patterns
endpoints = [
    'https://dulceriasdenny.com/api/productos',
    'https://dulceriasdenny.com/api/products',
    'https://dulceriasdenny.com/productos/api',
    'https://dulceriasdenny.com/productos/json',
    'https://dulceriasdenny.com/wp-json/wp/v2/product',
    'https://dulceriasdenny.com/wp-json/wc/v3/products',
]

for endpoint in endpoints:
    try:
        r = requests.get(endpoint, headers=headers, timeout=5)
        print(f"{endpoint}")
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  JSON response: {json.dumps(data, indent=2)[:200]}")
            except:
                print(f"  Response (first 200 chars): {r.text[:200]}")
        print()
    except Exception as e:
        print(f"{endpoint}: Error - {e}\n")
