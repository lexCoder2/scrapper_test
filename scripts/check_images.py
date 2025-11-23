"""
Quick script to check image status in database
"""

from pymongo import MongoClient

mongodb_uri = "mongodb://admin:productdb2025@localhost:27017/products?authSource=admin"
client = MongoClient(mongodb_uri)
db = client['products']
collection = db['grocery_products']

total = collection.count_documents({})
no_url = collection.count_documents({'$or': [{'image_url': ''}, {'image_url': None}, {'image_url': {'$exists': False}}]})
has_url = total - no_url

# Check local_image field
local_is_url = collection.count_documents({'local_image': {'$regex': '^http'}})
local_is_path = collection.count_documents({'local_image': {'$regex': '^product_images'}})
local_empty = collection.count_documents({'$or': [{'local_image': ''}, {'local_image': None}, {'local_image': {'$exists': False}}]})

print("="*60)
print("IMAGE STATUS IN DATABASE")
print("="*60)
print(f"Total products: {total}")
print(f"Products with image_url: {has_url}")
print(f"Products without image_url: {no_url}")
print()
print(f"local_image is URL (needs download): {local_is_url}")
print(f"local_image is local path: {local_is_path}")
print(f"local_image is empty/missing: {local_empty}")
print("="*60)

# Sample some products
print("\nSample products by store:")
for store in ['Chedraui', 'La Comer', 'Papelerias Tony']:
    doc = collection.find_one({'store': store})
    if doc:
        print(f"\n{store}:")
        print(f"  SKU: {doc.get('sku')}")
        print(f"  Image URL: {doc.get('image_url', 'N/A')[:80]}")
        print(f"  Local Image: {doc.get('local_image', 'N/A')[:80]}")
