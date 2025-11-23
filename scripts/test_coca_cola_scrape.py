"""
Test script to fetch one Coca-Cola product from each store
"""
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_chedraui():
    """Get Coca-Cola from Chedraui (VTEX)"""
    print("\n" + "="*60)
    print("CHEDRAUI - Coca-Cola Product")
    print("="*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    # Search for Coca-Cola - using REST API with pagination
    url = "https://www.chedraui.com.mx/api/catalog_system/pub/products/search"
    
    try:
        response = requests.get(url, headers=headers, timeout=15, params={
            'ft': 'coca cola',
            '_from': 0,
            '_to': 0
        })
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            if products:
                # Get first product
                item = products[0]
                
                # Extract data like the scraper does
                sku = str(item.get('productId', ''))
                name = item.get('productName', '')
                brand = item.get('brand', '')
                
                # Get price from first SKU
                skus = item.get('items', [])
                price = 0
                image_url = ''
                api_ean = ''
                ref_code = ''
                
                if skus:
                    first_sku = skus[0]
                    sellers = first_sku.get('sellers', [])
                    if sellers:
                        price = sellers[0].get('commertialOffer', {}).get('Price', 0)
                    
                    images = first_sku.get('images', [])
                    if images:
                        image_url = images[0].get('imageUrl', '')
                    
                    api_ean = first_sku.get('ean')
                    ref_code = first_sku.get('referenceId', [{}])[0].get('Value')
                
                # Build product like scraper does
                product = {
                    'sku': sku,
                    'ean': str(api_ean) if api_ean else '',
                    'upc': '',
                    'ean13': '',
                    'reference': str(ref_code) if ref_code else '',
                    'product_id': str(item.get('productId', '')),
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'currency': 'MXN',
                    'category': item.get('categories', [''])[0] if item.get('categories') else '',
                    'store': 'Chedraui',
                    'url': f"https://www.chedraui.com.mx/{item.get('linkText', '')}/p",
                    'image_url': image_url,
                    'local_image': image_url,  # Would be path if downloaded
                    'in_stock': True,
                    'scraped_at': '2025-11-19'
                }
                
                print(json.dumps(product, indent=2, ensure_ascii=False))
                return product
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_lacomer():
    """Get Coca-Cola from La Comer (Amarello)"""
    print("\n" + "="*60)
    print("LA COMER - Coca-Cola Product")
    print("="*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    url = "https://www.lacomer.com.mx/lacomerv2/api/products"
    
    try:
        response = requests.get(url, headers=headers, timeout=15, params={
            'wholesaler': 'LACOMER',
            'search': 'coca cola',
            'page': 1,
            'perPage': 1
        })
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            
            if products:
                item = products[0]
                
                product = {
                    'sku': str(item.get('articleCode', '')),
                    'ean': '',
                    'upc': '',
                    'ean13': item.get('ean13', ''),
                    'reference': str(item.get('articleCode', '')),
                    'product_id': str(item.get('id', '')),
                    'name': item.get('name', ''),
                    'brand': item.get('brand', ''),
                    'price': float(item.get('price', {}).get('beforeTaxes', 0)),
                    'currency': 'MXN',
                    'category': item.get('category', {}).get('name', ''),
                    'store': 'La Comer',
                    'url': f"https://www.lacomer.com.mx/lacomer/producto/{item.get('slug', '')}",
                    'image_url': item.get('image', {}).get('url', ''),
                    'local_image': item.get('image', {}).get('url', ''),
                    'in_stock': item.get('stock', {}).get('isAvailable', False),
                    'scraped_at': '2025-11-19'
                }
                
                print(json.dumps(product, indent=2, ensure_ascii=False))
                return product
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_tony():
    """Get Coca-Cola from Papelerias Tony (VTEX)"""
    print("\n" + "="*60)
    print("PAPELERIAS TONY - Coca-Cola Product")
    print("="*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    url = "https://www.papeleriatony.com.mx/api/catalog_system/pub/products/search"
    
    try:
        response = requests.get(url, headers=headers, timeout=15, params={
            'ft': 'coca cola',
            '_from': 0,
            '_to': 0
        }, verify=False)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            products = response.json()
            if products:
                item = products[0]
                
                sku = str(item.get('productId', ''))
                name = item.get('productName', '')
                brand = item.get('brand', '')
                
                skus = item.get('items', [])
                price = 0
                image_url = ''
                api_ean = ''
                
                if skus:
                    first_sku = skus[0]
                    sellers = first_sku.get('sellers', [])
                    if sellers:
                        price = sellers[0].get('commertialOffer', {}).get('Price', 0)
                    
                    images = first_sku.get('images', [])
                    if images:
                        image_url = images[0].get('imageUrl', '')
                    
                    api_ean = first_sku.get('ean')
                
                product = {
                    'sku': sku,
                    'ean': str(api_ean) if api_ean else '',
                    'upc': '',
                    'ean13': '',
                    'reference': '',
                    'product_id': str(item.get('productId', '')),
                    'name': name,
                    'brand': brand,
                    'price': price,
                    'currency': 'MXN',
                    'category': item.get('categories', [''])[0] if item.get('categories') else '',
                    'store': 'Papelerias Tony',
                    'url': f"https://www.papeleriatony.com.mx/{item.get('linkText', '')}/p",
                    'image_url': image_url,
                    'local_image': image_url,
                    'in_stock': True,
                    'scraped_at': '2025-11-19'
                }
                
                print(json.dumps(product, indent=2, ensure_ascii=False))
                return product
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def test_dulces_balu():
    """Get Coca-Cola from Dulces Balu (Shopify)"""
    print("\n" + "="*60)
    print("DULCES BALU - Coca-Cola Product")
    print("="*60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    url = "https://dulcesbalu.mx/search/suggest.json"
    
    try:
        response = requests.get(url, headers=headers, timeout=15, params={
            'q': 'coca cola',
            'resources[type]': 'product',
            'resources[limit]': 1
        })
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {data.keys()}")
            products = data.get('resources', {}).get('results', {}).get('products', [])
            print(f"Products found: {len(products)}")
            
            if products:
                item = products[0]
                
                # Get first variant
                variant = item.get('variants', [{}])[0] if item.get('variants') else {}
                
                product = {
                    'sku': str(variant.get('sku', '')),
                    'ean': str(variant.get('barcode', '')),
                    'upc': str(variant.get('barcode', '')),
                    'ean13': str(variant.get('barcode', '')),
                    'reference': str(variant.get('sku', '')),
                    'product_id': str(item.get('id', '')),
                    'name': item.get('title', ''),
                    'brand': item.get('vendor', ''),
                    'price': float(variant.get('price', 0)) / 100,
                    'currency': 'MXN',
                    'category': item.get('product_type', ''),
                    'store': 'Dulces Balu',
                    'url': f"https://dulcesbalu.mx{item.get('url', '')}",
                    'image_url': f"https:{item.get('image', '')}" if item.get('image', '').startswith('//') else item.get('image', ''),
                    'local_image': f"https:{item.get('image', '')}" if item.get('image', '').startswith('//') else item.get('image', ''),
                    'in_stock': variant.get('available', False),
                    'scraped_at': '2025-11-19'
                }
                
                print(json.dumps(product, indent=2, ensure_ascii=False))
                return product
    except Exception as e:
        print(f"Error: {e}")
    
    return None

if __name__ == "__main__":
    print("\n")
    print("="*60)
    print("TESTING COCA-COLA SCRAPING FROM EACH STORE")
    print("="*60)
    
    results = {
        'Chedraui': test_chedraui(),
        'La Comer': test_lacomer(),
        'Papelerias Tony': test_tony(),
        'Dulces Balu': test_dulces_balu()
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for store, product in results.items():
        if product:
            print(f"✓ {store}: {product['name']} - ${product['price']} MXN")
        else:
            print(f"✗ {store}: No product found")
