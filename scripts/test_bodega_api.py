import requests
import json

# Test Bodega Aurrera API (Walmart Mexico)
# Try different potential endpoints

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9'
}

# Test 1: Walmart Mexico API
print("Testing Walmart Mexico (Bodega Aurrera) API...")
print("="*60)

urls_to_test = [
    {
        'name': 'Walmart Mexico Search',
        'url': 'https://www.bodegaaurrera.com.mx/_v/public/graphql/v1',
        'method': 'POST',
        'data': {
            "query": "query SearchQuery($query: String!, $page: Int) { search(query: $query, page: $page) { products { productId productName brand description } } }",
            "variables": {"query": "leche", "page": 1}
        }
    },
    {
        'name': 'Walmart API v2',
        'url': 'https://super.walmart.com.mx/api/v2/search',
        'method': 'GET',
        'params': {'q': 'leche', 'page': 1}
    },
    {
        'name': 'Bodega Aurrera VTEX',
        'url': 'https://www.bodegaaurrera.com.mx/api/catalog_system/pub/products/search',
        'method': 'GET',
        'params': {'q': 'leche', '_from': 0, '_to': 49}
    }
]

for test in urls_to_test:
    print(f"\nTest: {test['name']}")
    print(f"URL: {test['url']}")
    try:
        if test['method'] == 'POST':
            response = requests.post(
                test['url'], 
                json=test.get('data'),
                headers={**headers, 'Content-Type': 'application/json'},
                timeout=10
            )
        else:
            response = requests.get(
                test['url'],
                params=test.get('params', {}),
                headers=headers,
                timeout=10
            )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response keys: {list(data.keys()) if isinstance(data, dict) else 'List response'}")
                print(f"\nFirst 500 chars:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
            except:
                print(f"Response (first 300 chars): {response.text[:300]}")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")
    print("-"*60)
