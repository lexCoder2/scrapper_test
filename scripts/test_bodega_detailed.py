import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9'
}

print("Testing Bodega Aurrera VTEX API...")
print("="*60)

# Test different endpoints
tests = [
    {
        'name': 'VTEX buscaglobal',
        'url': 'https://www.bodegaaurrera.com.mx/buscaglobal',
        'params': {'ft': 'Abarrotes', '_from': 0, '_to': 49, 'O': 'OrderByTopSaleDESC'}
    },
    {
        'name': 'VTEX catalog search',
        'url': 'https://www.bodegaaurrera.com.mx/api/catalog_system/pub/products/search',
        'params': {'ft': 'leche', '_from': 0, '_to': 49}
    },
    {
        'name': 'VTEX category',
        'url': 'https://www.bodegaaurrera.com.mx/api/catalog_system/pub/products/search',
        'params': {'fq': 'C:/1/', '_from': 0, '_to': 49}
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
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"Result: List with {len(data)} items")
                    if data:
                        print(f"\nFirst item keys: {list(data[0].keys())}")
                        print(f"First product: {data[0].get('productName', 'No name')}")
                elif isinstance(data, dict):
                    print(f"Result: Dict with keys: {list(data.keys())}")
            except:
                print(f"Response (first 300 chars): {response.text[:300]}")
        else:
            print(f"Error: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
    
    print("-"*60)
