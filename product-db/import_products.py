"""
Import products from JSON to MongoDB
"""

import json
from pymongo import MongoClient
from datetime import datetime
import sys

def import_products(json_file, mongodb_uri):
    """Import products from JSON file to MongoDB"""
    
    print(f"Loading products from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Loaded {len(products)} products")
    
    print(f"Connecting to MongoDB...")
    client = MongoClient(mongodb_uri)
    db = client['products']
    collection = db['grocery_products']
    
    print("Importing products...")
    
    # Use bulk operations for better performance
    from pymongo import UpdateOne
    
    operations = []
    for product in products:
        # Remove _id if it exists to avoid conflicts
        if '_id' in product:
            del product['_id']
        
        operation = UpdateOne(
            {'sku': product['sku']},
            {'$set': product},
            upsert=True
        )
        operations.append(operation)
        
        # Execute in batches of 1000
        if len(operations) >= 1000:
            result = collection.bulk_write(operations, ordered=False)
            print(f"  Imported {len(operations)} products (upserted: {result.upserted_count}, modified: {result.modified_count})")
            operations = []
    
    # Import remaining products
    if operations:
        result = collection.bulk_write(operations, ordered=False)
        print(f"  Imported {len(operations)} products (upserted: {result.upserted_count}, modified: {result.modified_count})")
    
    # Get final count
    total = collection.count_documents({})
    print(f"\n✓ Import complete! Total products in database: {total}")
    
    # Create indexes
    print("\nCreating indexes...")
    collection.create_index([('sku', 1)], unique=True)
    collection.create_index([('ean13', 1)])
    collection.create_index([('upc', 1)])
    collection.create_index([('name', 'text'), ('brand', 'text'), ('category', 'text')])
    collection.create_index([('store', 1)])
    collection.create_index([('category', 1)])
    collection.create_index([('brand', 1)])
    collection.create_index([('price', 1)])
    print("✓ Indexes created")
    
    client.close()

if __name__ == "__main__":
    # Configuration
    json_file = "../simple-scanner-app/grocery-products.json"
    mongodb_uri = "mongodb://admin:productdb2025@localhost:27017/products?authSource=admin"
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        mongodb_uri = sys.argv[2]
    
    print("Product Import Tool")
    print("=" * 60)
    print(f"Source: {json_file}")
    print(f"MongoDB URI: {mongodb_uri}")
    print("=" * 60)
    
    try:
        import_products(json_file, mongodb_uri)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
