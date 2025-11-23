from pymongo import MongoClient

client = MongoClient('mongodb://admin:productdb2025@localhost:27017/products?authSource=admin')
db = client['products']

count = db['grocery_products'].count_documents({})
print(f'Total products in DB: {count}')

stores = db['grocery_products'].aggregate([
    {'$group': {'_id': '$store', 'count': {'$sum': 1}}}
])

print('\nProducts per store:')
for s in stores:
    print(f"  {s['_id']}: {s['count']}")
