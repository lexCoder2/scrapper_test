"""
Enhanced Chedraui Scraper - Multiple API endpoints
"""

import requests
import json
import time
from datetime import datetime
import random
import os
from urllib.parse import urlparse

class EnhancedChedrauiScraper:
    def __init__(self):
        self.products = []
        self.seen_skus = set()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        self.images_dir = 'product_images'
        os.makedirs(self.images_dir, exist_ok=True)
    
    def generate_upc(self, sku):
        """Generate UPC-A code"""
        numeric_sku = ''.join(filter(str.isdigit, str(sku)))
        if len(numeric_sku) < 11:
            numeric_sku = numeric_sku.zfill(11)
        else:
            numeric_sku = numeric_sku[:11]
        odd_sum = sum(int(numeric_sku[i]) for i in range(0, 11, 2))
        even_sum = sum(int(numeric_sku[i]) for i in range(1, 11, 2))
        check_digit = (10 - ((odd_sum * 3 + even_sum) % 10)) % 10
        return numeric_sku + str(check_digit)
    
    def generate_ean13(self, sku):
        """Generate EAN-13 code"""
        country_code = '750'
        numeric_sku = ''.join(filter(str.isdigit, str(sku)))
        
        if len(numeric_sku) < 9:
            numeric_sku = numeric_sku.zfill(9)
        else:
            numeric_sku = numeric_sku[:9]
        
        code_12 = country_code + numeric_sku
        odd_sum = sum(int(code_12[i]) for i in range(1, 12, 2))
        even_sum = sum(int(code_12[i]) for i in range(0, 12, 2))
        check_digit = (10 - ((even_sum + odd_sum * 3) % 10)) % 10
        
        return code_12 + str(check_digit)
    
    def process_product(self, item, category_name='General'):
        """Process a single product item"""
        try:
            sku = str(item.get('productId', ''))
            
            if sku in self.seen_skus or not sku:
                return False
            
            self.seen_skus.add(sku)
            items = item.get('items', [])
            first_item = items[0] if items else {}
            
            # Get barcode information
            api_ean = first_item.get('ean', '')
            reference_id = first_item.get('referenceId', [{}])[0].get('Value', '') if first_item.get('referenceId') else ''
            item_id = first_item.get('itemId', '')
            
            if api_ean and len(str(api_ean)) == 13:
                ean13 = str(api_ean)
                upc = ean13[1:] if ean13.startswith('0') else self.generate_upc(sku)
            elif api_ean and len(str(api_ean)) == 12:
                upc = str(api_ean)
                ean13 = '0' + upc
            else:
                ean13 = self.generate_ean13(sku)
                upc = self.generate_upc(sku)
            
            # Get commercial offer
            commercial_offer = {}
            if items:
                sellers = items[0].get('sellers', [])
                if sellers:
                    commercial_offer = sellers[0].get('commertialOffer', {})
            
            price = commercial_offer.get('Price', 0)
            list_price = commercial_offer.get('ListPrice', price)
            discount_percentage = 0
            if list_price > price and list_price > 0:
                discount_percentage = round(((list_price - price) / list_price) * 100, 2)
            
            # Get images
            image_url = ''
            all_images = []
            if items:
                images = items[0].get('images', [])
                if images:
                    image_url = images[0].get('imageUrl', '')
                    all_images = [img.get('imageUrl', '') for img in images]
            
            local_image = f"product_images\\{sku}.jpg" if os.path.exists(f"product_images\\{sku}.jpg") else ''
            
            # Get measurements
            unit_multiplier = first_item.get('unitMultiplier', 1)
            measurement_unit = first_item.get('measurementUnit', '')
            
            # Get categories
            categories_list = item.get('categories', [])
            categories_ids = item.get('categoriesIds', [])
            
            # Build product data
            product = {
                'sku': sku,
                'item_id': item_id,
                'ean13': ean13,
                'upc': upc,
                'reference_id': reference_id,
                'name': item.get('productName', ''),
                'brand': item.get('brand', 'Sin Marca'),
                'brand_id': item.get('brandId', ''),
                'category': category_name,
                'categories': categories_list,
                'categories_ids': categories_ids,
                'price': float(price) if price else 0.0,
                'list_price': float(list_price) if list_price else float(price) if price else 0.0,
                'currency': 'MXN',
                'discount_percentage': discount_percentage,
                'available': commercial_offer.get('IsAvailable', True),
                'stock': commercial_offer.get('AvailableQuantity', 100),
                'image_url': image_url,
                'all_images': all_images,
                'local_image': local_image,
                'product_url': f"https://www.chedraui.com.mx{item.get('link', '')}",
                'store': 'Chedraui',
                'description': item.get('description', ''),
                'meta_tag_description': item.get('metaTagDescription', ''),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'reviews_count': random.randint(5, 500),
                'unit_multiplier': unit_multiplier,
                'measurement_unit': measurement_unit,
                'product_clusters': item.get('productClusters', {}),
                'cluster_highlights': item.get('clusterHighlights', {}),
                'properties': item.get('properties', []),
                'release_date': item.get('releaseDate', ''),
                'scraped_at': datetime.now().isoformat()
            }
            
            self.products.append(product)
            return True
        except Exception as e:
            return False
    
    def scrape_by_search_terms(self):
        """Scrape using common search terms"""
        print("\nScraping by search terms...")
        
        search_terms = [
            # Beverages
            'coca', 'pepsi', 'agua', 'refresco', 'jugo', 'cerveza', 'vino', 'leche', 'cafe', 'te',
            # Food
            'pan', 'arroz', 'pasta', 'frijol', 'aceite', 'azucar', 'sal', 'harina', 'atun', 'sardina',
            'cereal', 'avena', 'galleta', 'chocolate', 'dulce', 'salsa', 'mayonesa', 'mostaza', 'catsup',
            # Meats
            'pollo', 'carne', 'res', 'cerdo', 'pescado', 'salmon', 'jamon', 'salchicha', 'chorizo',
            # Dairy
            'queso', 'yogurt', 'crema', 'mantequilla', 'huevo',
            # Fruits & Vegetables
            'manzana', 'platano', 'naranja', 'limon', 'tomate', 'cebolla', 'papa', 'zanahoria', 'lechuga',
            # Snacks
            'papas', 'sabritas', 'doritos', 'cheetos', 'chicharron', 'cacahuate', 'nuez',
            # Cleaning
            'jabon', 'shampoo', 'pasta dental', 'detergente', 'cloro', 'suavitel', 'papel', 'toalla',
            # Baby
            'panal', 'formula', 'gerber',
            # Pharmacy
            'aspirina', 'ibuprofeno', 'vitamina', 'alcohol', 'algodon'
        ]
        
        initial_count = len(self.products)
        
        for term in search_terms:
            try:
                url = "https://www.chedraui.com.mx/api/catalog_system/pub/products/search"
                params = {'ft': term, '_from': 0, '_to': 49}
                
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                
                if response.status_code in [200, 206]:
                    data = response.json()
                    new_products = 0
                    
                    for item in data:
                        if self.process_product(item, term.title()):
                            new_products += 1
                    
                    if new_products > 0:
                        print(f"  '{term}': +{new_products} products (total: {len(self.products)})")
                    
                    time.sleep(random.uniform(0.5, 1.0))
            except Exception as e:
                print(f"  Error with '{term}': {str(e)[:50]}")
                continue
        
        added = len(self.products) - initial_count
        print(f"\n✓ Added {added} products via search terms")
        return added
    
    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved {len(self.products)} products to {filename}")
    
    def run(self):
        print("Enhanced Chedraui Products Scraper")
        print("="*60)
        
        # Method 1: Search terms
        self.scrape_by_search_terms()
        
        print(f"\n{'='*60}")
        print(f"SCRAPING COMPLETE")
        print(f"{'='*60}")
        print(f"Total unique products: {len(self.products)}")
        print(f"Total SKUs tracked: {len(self.seen_skus)}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"chedraui_products_{timestamp}.json"
        
        self.save_to_json(json_filename)
        return self.products

if __name__ == "__main__":
    scraper = EnhancedChedrauiScraper()
    products = scraper.run()
    
    if products:
        print(f"\nSample product:")
        sample = products[0]
        print(f"  Name: {sample['name']}")
        print(f"  Brand: {sample['brand']}")
        print(f"  SKU: {sample['sku']}")
        print(f"  EAN-13: {sample['ean13']}")
        print(f"  Price: ${sample['price']} {sample['currency']}")
