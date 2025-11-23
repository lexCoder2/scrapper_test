#!/usr/bin/env python3
"""
Get one complete product example from each store
"""
import sys
import json
from pathlib import Path
from pymongo import MongoClient

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "products"
COLLECTION_NAME = "grocery_products"

def get_product_examples():
    """Get one product example from each store"""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        stores = ["Chedraui", "La Comer", "Papelerias Tony", "Dulces Balu"]
        examples = {}
        
        for store in stores:
            product = collection.find_one({"store": store})
            if product:
                # Remove MongoDB _id for cleaner output
                if "_id" in product:
                    product["_id"] = str(product["_id"])
                examples[store] = product
            else:
                examples[store] = None
        
        # Print as JSON
        print(json.dumps(examples, indent=2, ensure_ascii=False, default=str))
        
        client.close()
        return examples
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    get_product_examples()
