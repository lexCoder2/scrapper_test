import requests
import json

print("Testing Papelerias Tony pagination...\n")

for page in range(0, 3):
    _from = page * 50
    _to = _from + 49
    
    url = "https://www.tony.com.mx/api/catalog_system/pub/products/search"
    params = {
        'ft': 'escolar',
        '_from': _from,
        '_to': _to
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Page {page} (_from={_from}, _to={_to}): Status {r.status_code}, Products: {len(r.json())}")
        if r.json():
            first = r.json()[0]
            print(f"  First product: {first.get('productId')} - {first.get('productName')}")
    except Exception as e:
        print(f"Page {page}: Error - {e}")
