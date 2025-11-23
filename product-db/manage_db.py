"""
Product Database Management Tool
"""

from pymongo import MongoClient
import sys

MONGODB_URI = "mongodb://admin:productdb2025@localhost:27017/products?authSource=admin"

def connect():
    """Connect to MongoDB"""
    client = MongoClient(MONGODB_URI)
    return client['products']['grocery_products']

def show_stats():
    """Show database statistics"""
    collection = connect()
    
    total = collection.count_documents({})
    stores = collection.distinct('store')
    brands = collection.distinct('brand')
    categories = collection.distinct('category')
    
    print("="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    print(f"Total Products: {total:,}")
    print(f"Stores: {len(stores)}")
    print(f"Brands: {len(brands)}")
    print(f"Categories: {len(categories)}")
    print("\nStores:", ", ".join(stores))
    print("="*60)

def search_product(query):
    """Search for products"""
    collection = connect()
    
    # Try barcode search first
    product = collection.find_one({
        '$or': [
            {'ean13': query},
            {'upc': query},
            {'sku': query}
        ]
    })
    
    if product:
        print("\n✓ Product found by barcode:")
        print(f"  Name: {product['name']}")
        print(f"  Brand: {product['brand']}")
        print(f"  SKU: {product['sku']}")
        print(f"  EAN-13: {product.get('ean13', 'N/A')}")
        print(f"  UPC: {product.get('upc', 'N/A')}")
        print(f"  Price: ${product['price']} {product['currency']}")
        return
    
    # Text search
    results = list(collection.find(
        {'$text': {'$search': query}},
        {'score': {'$meta': 'textScore'}}
    ).sort([('score', {'$meta': 'textScore'})]).limit(5))
    
    if results:
        print(f"\n✓ Found {len(results)} products:")
        for i, p in enumerate(results, 1):
            print(f"\n{i}. {p['name']}")
            print(f"   Brand: {p['brand']}")
            print(f"   SKU: {p['sku']} | EAN-13: {p.get('ean13', 'N/A')}")
            print(f"   Price: ${p['price']} {p['currency']}")
    else:
        print("\n✗ No products found")

def clear_database():
    """Clear all products from database"""
    collection = connect()
    
    count = collection.count_documents({})
    print(f"This will delete {count:,} products from the database.")
    confirm = input("Are you sure? (yes/no): ")
    
    if confirm.lower() == 'yes':
        result = collection.delete_many({})
        print(f"✓ Deleted {result.deleted_count:,} products")
    else:
        print("Cancelled")

def list_categories():
    """List all categories"""
    collection = connect()
    
    categories = collection.distinct('category')
    categories.sort()
    
    print("\n" + "="*60)
    print("CATEGORIES")
    print("="*60)
    for i, cat in enumerate(categories, 1):
        count = collection.count_documents({'category': cat})
        print(f"{i:2d}. {cat:30s} ({count:,} products)")
    print("="*60)

def main():
    """Main menu"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'stats':
            show_stats()
        elif command == 'search' and len(sys.argv) > 2:
            search_product(' '.join(sys.argv[2:]))
        elif command == 'clear':
            clear_database()
        elif command == 'categories':
            list_categories()
        else:
            print("Unknown command")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Print usage information"""
    print("\nProduct Database Management Tool")
    print("="*60)
    print("\nUsage:")
    print("  python manage_db.py stats              - Show database statistics")
    print("  python manage_db.py search <query>     - Search for products")
    print("  python manage_db.py categories         - List all categories")
    print("  python manage_db.py clear              - Clear database")
    print("\nExamples:")
    print("  python manage_db.py search coca cola")
    print("  python manage_db.py search 2502958000005")
    print("="*60)

if __name__ == "__main__":
    main()
