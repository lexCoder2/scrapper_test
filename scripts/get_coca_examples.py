import requests
import json
import urllib3
urllib3.disable_warnings()

# Get one Coca-Cola product from each store via API
response = requests.get('https://localhost:3443/api/products/all', verify=False, timeout=10)

if response.status_code == 200:
    all_products = response.json()
    
    stores = ['Chedraui', 'La Comer', 'Papelerias Tony', 'Dulces Balu']
    examples = {}
    
    for store in stores:
        # Find first Coca-Cola product from this store
        for product in all_products:
            if product['store'] == store and 'coca' in product['name'].lower():
                examples[store] = product
                break
    
    # Print examples
    print(json.dumps(examples, indent=2, ensure_ascii=False))
else:
    print(f"API Error: {response.status_code}")
