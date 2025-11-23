# 🛒 Mexico Grocery Products - Quick Start Guide

## ✅ Success! You now have product data!

### 📊 What You Have

**Real scraped data from Chedraui:**

- File: `mexico_grocery_products_20251118_161930.csv` / `.json`
- Products: 131 real products from Chedraui Mexico
- Includes: Real SKUs, prices, brands, categories, availability

**Sample realistic data:**

- File: `mexico_grocery_sample_20251118_162048.csv` / `.json`
- Products: 2,000 realistic Mexican grocery products
- Stores: Soriana, Walmart, Chedraui, HEB, Bodega Aurrera, etc.
- Categories: Bebidas, Lácteos, Despensa, Carnes, Limpieza, etc.
- Features: Realistic prices, brands, discounts, ratings

---

## 🚀 Quick Commands

### Generate More Sample Data

```powershell
python scripts/generate_sample_products.py
```

### Try Scraping Again

```powershell
python scripts/scrape_grocery_products.py
```

---

## 📋 Data Fields Available

Both datasets include:

| Field         | Description                        |
| ------------- | ---------------------------------- |
| `sku`         | Product SKU/ID                     |
| `name`        | Full product name with size        |
| `brand`       | Brand name (Coca-Cola, Lala, etc.) |
| `category`    | Category (Bebidas, Lácteos, etc.)  |
| `price`       | Current selling price (MXN)        |
| `list_price`  | Original list price (MXN)          |
| `available`   | In stock (true/false)              |
| `store`       | Store name                         |
| `image_url`   | Product image URL                  |
| `product_url` | Link to product page               |
| `description` | Product description                |

**Sample data also includes:**

- `discount_percentage` - Discount amount
- `rating` - Customer rating (1-5)
- `reviews_count` - Number of reviews
- `stock_quantity` - Items in stock
- `upc` - Universal Product Code

---

## 📂 Files Created

```
n8n/
├── mexico_grocery_products_20251118_161930.csv  ← Real Chedraui data
├── mexico_grocery_products_20251118_161930.json
├── mexico_grocery_sample_20251118_162048.csv    ← Sample data (2000 products)
├── mexico_grocery_sample_20251118_162048.json
└── scripts/
    ├── scrape_grocery_products.py               ← Web scraper
    └── generate_sample_products.py              ← Sample generator
```

---

## 💡 How to Use the Data

### 1. Open in Excel

```powershell
# CSV files open directly in Excel
start mexico_grocery_sample_20251118_162048.csv
```

### 2. Load in Python

```python
import pandas as pd

# Load CSV
df = pd.read_csv('mexico_grocery_sample_20251118_162048.csv')
print(df.head())
print(f"Total products: {len(df)}")

# Filter by category
bebidas = df[df['category'] == 'Bebidas']
print(f"Bebidas: {len(bebidas)}")

# Get average price by store
avg_prices = df.groupby('store')['price'].mean()
print(avg_prices)
```

### 3. Load JSON

```python
import json

with open('mexico_grocery_sample_20251118_162048.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Total products: {len(products)}")
print(products[0])  # First product
```

### 4. Import to n8n

1. Open http://localhost:5678
2. Create a new workflow
3. Add "Read Binary File" node
4. Point to the JSON file
5. Add "JSON" node to parse it
6. Use the data in your automation

### 5. Import to Database

```python
import sqlite3
import pandas as pd

df = pd.read_csv('mexico_grocery_sample_20251118_162048.csv')
conn = sqlite3.connect('grocery_products.db')
df.to_sql('products', conn, if_exists='replace', index=False)
conn.close()
```

---

## 🎯 Why Some Stores Don't Work

**Current Status:**

- ✅ **Chedraui** - Working! Got 131 real products
- ❌ **Soriana** - API returns 404 (endpoint changed or requires authentication)
- ❌ **Walmart** - Returns 521 (web application firewall blocking automated requests)

**Solution:** Use the sample data generator for comprehensive datasets, or try scraping at different times when stores may have different security settings.

---

## 🔧 Customization

### Generate More/Less Products

Edit `generate_sample_products.py`:

```python
products = generate_mexican_grocery_products(count=5000)  # Change count
```

### Add Your Own Categories

Edit the `categories_data` dictionary in `generate_sample_products.py`

### Try Different Stores

The scraper will automatically try multiple stores and combine results.

---

## 📊 Example Use Cases

1. **E-commerce Testing** - Test shopping cart, checkout, search functionality
2. **Price Comparison App** - Compare prices across stores
3. **Inventory Management** - Track stock levels and availability
4. **Data Analysis** - Analyze pricing trends, popular brands
5. **Machine Learning** - Train recommendation systems
6. **Reports & Dashboards** - Create visualizations with PowerBI/Tableau

---

## 🆘 Troubleshooting

**No real data scraped:**

- Store APIs may be down or have changed
- Use the sample data generator instead
- It creates realistic data based on actual Mexican products

**CSV encoding issues in Excel:**

- Files use UTF-8-BOM encoding for Excel compatibility
- Should open correctly in Excel

**Need more data:**

- Run `generate_sample_products.py` multiple times
- Edit the count parameter to generate more products

---

## ✨ Summary

You have **2,131 total products** across two datasets:

- 131 real products from Chedraui
- 2,000 realistic sample products

Both are ready to use in Excel, databases, n8n workflows, or your applications!

---

## 📞 Next Steps

1. ✅ Open the CSV files in Excel to explore
2. ✅ Import to your database or application
3. ✅ Create n8n workflows to process the data
4. ✅ Generate more sample data as needed

Happy coding! 🎉
