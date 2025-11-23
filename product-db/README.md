# Product Database - MongoDB with Docker

This setup provides a lightweight MongoDB database for storing and querying product data.

## Services

- **MongoDB** (port 27017): NoSQL database
- **Mongo Express** (port 8081): Web-based admin interface
- **Product API** (port 3000): REST API for products

## Quick Start

### 1. Start the services

```powershell
docker-compose up -d
```

### 2. Import products

```powershell
# Install pymongo if not already installed
pip install pymongo

# Import products
python import_products.py
```

### 3. Access services

- **API**: http://localhost:3000
- **Admin UI**: http://localhost:8081 (admin/admin)
- **MongoDB**: mongodb://admin:productdb2025@localhost:27017

## API Endpoints

### Get all products (paginated)

```
GET /api/products?page=1&limit=50
```

### Get all products (no pagination)

```
GET /api/products/all
```

### Search products

```
GET /api/products/search?q=coca+cola&limit=50
```

### Get product by barcode

```
GET /api/products/barcode/7500031028767
```

### Get product by SKU

```
GET /api/products/sku/3102876
```

### Get statistics

```
GET /api/stats
```

### Filter by store

```
GET /api/products/store/Chedraui
```

### Filter by category

```
GET /api/products/category/despensa
```

### Bulk import

```
POST /api/products/import
Content-Type: application/json

[{ product data }]
```

## Update Scanner App

Update `simple-scanner-app/app.js` to use the API:

```javascript
async function loadProducts() {
  try {
    const response = await fetch("http://localhost:3000/api/products/all");
    if (response.ok) {
      products = await response.json();
      console.log(`Loaded ${products.length} products from API`);
      updateStats();
      updateProductCount();
    }
  } catch (error) {
    console.error("Error loading products:", error);
  }
}

async function searchByBarcode(barcode) {
  try {
    const response = await fetch(
      `http://localhost:3000/api/products/barcode/${barcode}`
    );
    if (response.ok) {
      return await response.json();
    }
  } catch (error) {
    console.error("Error searching barcode:", error);
  }
  return null;
}
```

## Database Info

- **Database**: products
- **Collection**: grocery_products
- **Indexes**: sku, ean13, upc, name (text), brand (text), category (text), store, price

## Stop Services

```powershell
docker-compose down
```

## Stop and Remove Data

```powershell
docker-compose down -v
```
