import requests
import json
from bs4 import BeautifulSoup

# Test Dulces Balu website structure
base_url = "https://dulcesbalu.mx"

print("Testing Dulces Balu website...")
print("=" * 60)

# Test main page
try:
    response = requests.get(base_url, timeout=10, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    print(f"\n1. Main page status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for common e-commerce platforms
        page_content = response.text.lower()
        
        if 'shopify' in page_content:
            print("   Platform: Shopify detected")
        elif 'woocommerce' in page_content:
            print("   Platform: WooCommerce detected")
        elif 'vtex' in page_content:
            print("   Platform: VTEX detected")
        elif 'magento' in page_content:
            print("   Platform: Magento detected")
        
        # Look for API endpoints
        if '/api/' in page_content:
            print("   Found /api/ references")
        if '/products.json' in page_content or 'products.json' in page_content:
            print("   Found products.json references")
        
        # Check for product links
        product_links = soup.find_all('a', href=True)
        product_urls = [a['href'] for a in product_links if 'product' in a['href'].lower()]
        if product_urls:
            print(f"   Found {len(product_urls)} product links")
            print(f"   Example: {product_urls[0]}")

except Exception as e:
    print(f"   Error: {e}")

# Test Shopify API endpoints (most common)
print("\n2. Testing Shopify API endpoints...")
shopify_endpoints = [
    "/products.json",
    "/collections.json",
    "/api/2023-01/products.json"
]

for endpoint in shopify_endpoints:
    try:
        url = base_url + endpoint
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        print(f"   {endpoint}: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'products' in data:
                print(f"      Found {len(data['products'])} products")
                if data['products']:
                    product = data['products'][0]
                    print(f"      Sample product: {product.get('title', 'N/A')}")
                    print(f"      Keys: {list(product.keys())[:10]}")
            break
    except Exception as e:
        print(f"      Error: {e}")

# Test product search
print("\n3. Testing search functionality...")
search_terms = ["dulce", "chocolate", "galleta"]
for term in search_terms:
    try:
        url = f"{base_url}/search?q={term}&type=product"
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        print(f"   Search '{term}': Status {response.status_code}")
        break
    except Exception as e:
        print(f"      Error: {e}")

print("\n" + "=" * 60)
