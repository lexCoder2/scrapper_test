import requests
import json

print("Testing store APIs...\n")

# Test La Comer
print("=" * 60)
print("LA COMER TEST")
print("=" * 60)
try:
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
    r = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        products = data.get('res', [])
        print(f"Products returned: {len(products)}")
        if products:
            print(f"First product SKU: {products[0].get('artCod')}")
            print(f"First product name: {products[0].get('artDes')}")
except Exception as e:
    print(f"Error: {e}")

# Test Dulces Balu
print("\n" + "=" * 60)
print("DULCES BALU TEST")
print("=" * 60)
try:
    url = "https://dulcesbalu.mx/products.json?limit=250&page=1"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        products = data.get('products', [])
        print(f"Products returned: {len(products)}")
        if products:
            print(f"First product ID: {products[0].get('id')}")
            print(f"First product title: {products[0].get('title')}")
            print(f"First product variants: {len(products[0].get('variants', []))}")
except Exception as e:
    print(f"Error: {e}")

# Test Papelerias Tony
print("\n" + "=" * 60)
print("PAPELERIAS TONY TEST")
print("=" * 60)
try:
    url = "https://www.tony.com.mx/api/catalog_system/pub/products/search"
    params = {
        'ft': 'escolar',
        '_from': 0,
        '_to': 49
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Products returned: {len(data)}")
        if data:
            print(f"First product ID: {data[0].get('productId')}")
            print(f"First product name: {data[0].get('productName')}")
except Exception as e:
    print(f"Error: {e}")
