import requests
import json

# Test La Comer API
url = "https://lacomer.buscador.amarello.com.mx/searchArtPrior"
params = {
    'col': 'lacomer_2',
    'npagel': 40,
    'p': 1,
    'patrocinados': 'false',
    's': 'despensa',
    'succId': 287,
    'topsort': 'false'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("Testing La Comer API...")
print(f"URL: {url}")
print(f"Params: {params}\n")

try:
    response = requests.get(url, params=params, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("Response keys:", list(data.keys()))
        
        # Check for product data
        for key in ['res', 'vecArticulo', 'prods', 'products', 'articulos', 'items']:
            if key in data:
                print(f"\nFound products in key: {key}")
                print(f"Number of products: {len(data[key])}")
                print(f"Total products available: {data.get('total', 'unknown')}")
                print(f"Number of pages: {data.get('numpages', 'unknown')}")
                if data[key]:
                    print(f"\nFirst product:")
                    print(json.dumps(data[key][0], indent=2, ensure_ascii=False))
                    print(f"\nSecond product:")
                    print(json.dumps(data[key][1], indent=2, ensure_ascii=False))
                break
        else:
            print("\nNo standard product array found.")
    else:
        print("Error response:")
        print(response.text)
        
except Exception as e:
    print(f"Error: {e}")
