import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9'
}

print("Testing Papelerias Tony VTEX API - Detailed")
print("="*60)

url = 'https://www.tony.com.mx/api/catalog_system/pub/products/search'
params = {'ft': 'escolar', '_from': 0, '_to': 2}  # Just get 3 products

try:
    response = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code in [200, 206]:
        data = response.json()
        print(f"\nNumber of products: {len(data)}")
        
        if data:
            print(f"\nFirst product structure:")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
            
except Exception as e:
    print(f"Error: {e}")
