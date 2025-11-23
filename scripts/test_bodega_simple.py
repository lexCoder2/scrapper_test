import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9,en;q=0.8',
    'Referer': 'https://despensa.bodegaaurrera.com.mx/',
    'Origin': 'https://despensa.bodegaaurrera.com.mx'
}

print("Testing Bodega Aurrera Search API...")
print("="*60)

# Try the search endpoint
url = "https://despensa.bodegaaurrera.com.mx/api/v1/search"
params = {
    'q': 'leche',
    'limit': 10,
    'offset': 0
}

try:
    response = requests.get(url, params=params, headers=headers, timeout=15)
    print(f"Search API Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Content-Type: {response.headers.get('content-type')}")
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
    else:
        print(f"Error: {response.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*60)
print("Testing category browse...")
print("="*60)

# Try browsing categories
url2 = "https://despensa.bodegaaurrera.com.mx/api/v1/browse"
params2 = {
    'category': 'Abarrotes',
    'limit': 10
}

try:
    response2 = requests.get(url2, params=params2, headers=headers, timeout=15)
    print(f"Browse API Status: {response2.status_code}")
    if response2.status_code == 200:
        data2 = response2.json()
        print(f"Response keys: {list(data2.keys())}")
    else:
        print(f"Error: {response2.text[:300]}")
except Exception as e:
    print(f"Exception: {e}")
