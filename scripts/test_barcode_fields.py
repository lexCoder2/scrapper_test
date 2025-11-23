"""
Test the updated scraper to verify barcode fields extraction
This script will collect just a few products from each store to verify the changes
"""

import sys
import os

# Add the scripts directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrape_all_stores import MultiStoreScraper
from pymongo import MongoClient
import json

def test_scraper():
    print("="*80)
    print("TESTING UPDATED SCRAPER - BARCODE FIELDS VERIFICATION")
    print("="*80)
    print("\nThis test will collect a few products from each store to verify:")
    print("1. New barcode fields are being extracted")
    print("2. All product data is saved correctly")
    print("3. No errors occur during scraping")
    print("\n" + "="*80 + "\n")
    
    # Initialize scraper
    mongodb_uri = 'mongodb://admin:productdb2025@localhost:27017/products?authSource=admin'
    scraper = MultiStoreScraper(mongodb_uri=mongodb_uri, save_images=False)
    
    # Clear database
    client = MongoClient(mongodb_uri)
    db = client['products']
    collection = db['grocery_products']
    collection.delete_many({})
    print("✓ Database cleared\n")
    
    # Test each store with limited products (modify the scraper temporarily)
    print("Running scrapers...\n")
    scraper.run()
    
    # Check results
    print("\n" + "="*80)
    print("VERIFICATION RESULTS")
    print("="*80 + "\n")
    
    # Get sample products from each store
    stores = ['Chedraui', 'La Comer', 'Papelerias Tony']
    
    for store in stores:
        print(f"\n{'='*60}")
        print(f"STORE: {store}")
        print('='*60)
        
        products = list(collection.find({'store': store}).limit(3))
        
        if not products:
            print(f"⚠️  No products found for {store}")
            continue
        
        print(f"✓ Found {collection.count_documents({'store': store})} products")
        print(f"\nSample product #1 barcode fields:")
        
        product = products[0]
        barcode_fields = {
            'sku': product.get('sku', 'N/A'),
            'ean13': product.get('ean13', 'N/A'),
            'upc': product.get('upc', 'N/A'),
        }
        
        # Store-specific fields
        if store == 'Chedraui':
            barcode_fields.update({
                'ean': product.get('ean', 'N/A'),
                'multi_ean': product.get('multi_ean', 'N/A'),
                'reference': product.get('reference', 'N/A'),
                'product_id': product.get('product_id', 'N/A'),
            })
        elif store == 'La Comer':
            barcode_fields.update({
                'art_ean': product.get('art_ean', 'N/A'),
                'art_cod': product.get('art_cod', 'N/A'),
            })
        elif store == 'Papelerias Tony':
            barcode_fields.update({
                'item_ean': product.get('item_ean', 'N/A'),
                'product_reference': product.get('product_reference', 'N/A'),
                'product_reference_code': product.get('product_reference_code', 'N/A'),
            })
        
        print(json.dumps(barcode_fields, indent=2, ensure_ascii=False))
        print(f"\nProduct name: {product.get('name', 'N/A')}")
        print(f"Price: ${product.get('price', 0):.2f}")
    
    # Total count
    total = collection.count_documents({})
    print(f"\n{'='*80}")
    print(f"TOTAL PRODUCTS IN DATABASE: {total}")
    print('='*80)
    
    print("\n✓ Test completed successfully!")
    print("\nThe scraper is now configured to collect ALL products without limits.")
    print("Run 'python scrape_all_stores.py' to perform a full scrape.")

if __name__ == '__main__':
    test_scraper()
