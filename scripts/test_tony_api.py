import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9'
}

print("Testing Papelerias Tony API...")
print("="*60)

# Test different potential endpoints
tests = [
    {
        'name': 'VTEX buscaglobal',
        'url': 'https://www.tony.com.mx/buscaglobal',
        'params': {'ft': 'escolar', '_from': 0, '_to': 49}
    },
    {
        'name': 'VTEX catalog search',
        'url': 'https://www.tony.com.mx/api/catalog_system/pub/products/search',
        'params': {'ft': 'escolar', '_from': 0, '_to': 49}
    },
    {
        'name': 'VTEX search by category',
        'url': 'https://www.tony.com.mx/api/catalog_system/pub/products/search',
        'params': {'fq': 'C:/1/', '_from': 0, '_to': 49}
    },
    {
        'name': 'Direct category URL',
        'url': 'https://www.tony.com.mx/escolar',
        'params': {'_from': 0, '_to': 49}
    }
]

for test in tests:
    print(f"\nTest: {test['name']}")
    print(f"URL: {test['url']}")
    print(f"Params: {test['params']}")
    
    try:
        response = requests.get(test['url'], params=test['params'], headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"Result: List with {len(data)} items")
                        if data:
                            print(f"\nFirst item keys: {list(data[0].keys())}")
                            print(f"First product: {data[0].get('productName', data[0].get('name', 'No name'))}")
                            print(f"\nFull first item:")
                            print(json.dumps(data[0], indent=2, ensure_ascii=False)[:500])
                    elif isinstance(data, dict):
                        print(f"Result: Dict with keys: {list(data.keys())}")
                        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                except Exception as e:
                    print(f"JSON parse error: {e}")
                    print(f"Response (first 1000 chars): {response.text[:1000]}")
            else:
                print(f"HTML response (first 300 chars): {response.text[:300]}")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
    
    print("-"*60)
