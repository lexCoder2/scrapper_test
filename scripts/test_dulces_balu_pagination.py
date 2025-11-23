import requests
import json

base_url = "https://dulcesbalu.mx"

print("Testing Dulces Balu Shopify API pagination...")
print("=" * 60)

# Test pagination with limit and page parameters
page = 1
total_products = 0
all_products = []

print("\nFetching products with pagination...")

while page <= 5:  # Test first 5 pages
    try:
        # Shopify uses limit (max 250) and page parameters
        url = f"{base_url}/products.json?limit=250&page={page}"
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        print(f"\nPage {page}: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            if not products:
                print(f"   No more products found on page {page}")
                break
            
            print(f"   Found {len(products)} products")
            all_products.extend(products)
            total_products += len(products)
            
            # Show sample product structure
            if page == 1 and products:
                product = products[0]
                print(f"\n   Sample product structure:")
                print(f"   - ID: {product.get('id')}")
                print(f"   - Title: {product.get('title')}")
                print(f"   - Vendor: {product.get('vendor')}")
                print(f"   - Product Type: {product.get('product_type')}")
                print(f"   - Tags: {product.get('tags', [])}")
                print(f"   - Variants: {len(product.get('variants', []))}")
                
                if product.get('variants'):
                    variant = product['variants'][0]
                    print(f"\n   Sample variant structure:")
                    print(f"   - Price: {variant.get('price')}")
                    print(f"   - SKU: {variant.get('sku')}")
                    print(f"   - Barcode: {variant.get('barcode')}")
                    print(f"   - Weight: {variant.get('weight')}")
                
                if product.get('images'):
                    print(f"\n   Images: {len(product.get('images'))}")
                    print(f"   - First image: {product['images'][0].get('src')}")
        
        else:
            print(f"   Failed to fetch page {page}")
            break
        
        page += 1
        
    except Exception as e:
        print(f"   Error on page {page}: {e}")
        break

print(f"\n{'=' * 60}")
print(f"Total products found: {total_products}")
print(f"Unique products: {len(set(p['id'] for p in all_products))}")

# Check for collections endpoint
print(f"\n{'=' * 60}")
print("Testing collections endpoint...")
try:
    url = f"{base_url}/collections.json"
    response = requests.get(url, timeout=10, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        collections = data.get('collections', [])
        print(f"Found {len(collections)} collections")
        
        if collections:
            print("\nCollections:")
            for col in collections[:10]:
                print(f"   - {col.get('title')} (handle: {col.get('handle')})")
    
except Exception as e:
    print(f"Error: {e}")

print("=" * 60)
