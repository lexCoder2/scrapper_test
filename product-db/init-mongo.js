// MongoDB initialization script
db = db.getSiblingDB("products");

// Create collections
db.createCollection("grocery_products");

// Create indexes for efficient searching
db.grocery_products.createIndex({ sku: 1 }, { unique: true });
db.grocery_products.createIndex({ ean13: 1 });
db.grocery_products.createIndex({ upc: 1 });
db.grocery_products.createIndex({
  name: "text",
  brand: "text",
  category: "text",
});
db.grocery_products.createIndex({ store: 1 });
db.grocery_products.createIndex({ category: 1 });
db.grocery_products.createIndex({ brand: 1 });
db.grocery_products.createIndex({ price: 1 });

print("Database initialized successfully");
