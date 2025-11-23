# 📝 Mexican Stationery Products Dataset

## ✅ Successfully Generated: 2,000 Stationery Products

### 📊 Dataset Overview

**File:** `stationery_products_20251118_162642.csv` / `.json`
**Products:** 2,000 realistic Mexican stationery and office supply products
**Stores:** Office Depot, OfficeMax, Lumen, Papelería Cornejo, Walmart, Costco, Amazon México

---

## 📦 Product Categories (12 Categories)

| Category                     | Products | Examples                                              |
| ---------------------------- | -------- | ----------------------------------------------------- |
| **Escritura**                | 164      | Plumas, bolígrafos, marcadores, lápices, resaltadores |
| **Cuadernos y Libretas**     | 168      | Cuadernos profesionales, libretas, post-its, blocks   |
| **Hojas y Papel**            | 163      | Papel bond, fotográfico, cartulina, papel de colores  |
| **Archivado y Organización** | 180      | Carpetas, folders, archiveros, clasificadores         |
| **Adhesivos**                | 147      | Pegamento, cinta adhesiva, silicón, diurex            |
| **Artículos de Arte**        | 161      | Colores, plumones, acuarelas, plastilina, pinceles    |
| **Escritorio y Accesorios**  | 174      | Engrapadoras, perforadoras, tijeras, clips, grapas    |
| **Tecnología y Cómputo**     | 178      | Mouse, teclados, USB, cables, webcam, audífonos       |
| **Consumibles de Impresión** | 165      | Cartuchos, tóner, papel fotográfico, etiquetas        |
| **Mochilas y Loncheras**     | 171      | Mochilas escolares, loncheras, estuches               |
| **Calculadoras**             | 156      | Básicas, científicas, financieras                     |
| **Pizarrones**               | 173      | Pizarrones blancos, corcho, marcadores, borradores    |

---

## 🏷️ Featured Brands (71 Brands)

**Escritura:** Bic, Pelikan, Paper Mate, Pilot, Sharpie, Pentel, Stabilo, Faber-Castell, Staedtler

**Cuadernos:** Scribe, Norma, Loro, Oxford, Five Star, Kiut

**Tecnología:** HP, Logitech, Microsoft, Kingston, SanDisk, Verbatim

**Arte:** Prismacolor, Crayola, Faber-Castell, Giotto, Pelikan

**Mochilas:** Totto, JanSport, Kipling, Nike, Adidas, Puma

**Calculadoras:** Casio, Texas Instruments, HP, Canon, Sharp

---

## 📋 Data Fields

Each product includes:

| Field                 | Description                           |
| --------------------- | ------------------------------------- |
| `sku`                 | Product SKU (ST5000000+)              |
| `upc`                 | Universal Product Code                |
| `name`                | Full product name with brand and size |
| `brand`               | Brand name                            |
| `category`            | Main category                         |
| `subcategory`         | Product type                          |
| `size`                | Package size (pz, ml, hojas, etc.)    |
| `price`               | Current price (MXN)                   |
| `list_price`          | Original price (MXN)                  |
| `discount_percentage` | Discount amount (%)                   |
| `currency`            | MXN                                   |
| `available`           | Stock availability                    |
| `stock_quantity`      | Items in stock                        |
| `image_url`           | Product image URL                     |
| `product_url`         | Store product page                    |
| `store`               | Store name                            |
| `description`         | Product description                   |
| `rating`              | Customer rating (3.8-5.0)             |
| `reviews_count`       | Number of reviews                     |
| `is_school_supply`    | School supply indicator               |
| `is_office_supply`    | Office supply indicator               |
| `scraped_at`          | Timestamp                             |
| `last_updated`        | Last update timestamp                 |

---

## 💰 Price Statistics

- **Min Price:** $5.13 MXN (basic pens)
- **Max Price:** $1,499.71 MXN (financial calculators, printers)
- **Average Price:** $139.54 MXN
- **Products with Discounts:** 27.4%

---

## 🎯 Use Cases

### 1. Back-to-School Shopping Platform

Filter school supplies:

```python
import pandas as pd

df = pd.read_csv('stationery_products_20251118_162642.csv')
school_supplies = df[df['is_school_supply'] == True]
print(f"School supplies: {len(school_supplies)}")
```

### 2. Office Supply Management

Filter office products:

```python
office_supplies = df[df['is_office_supply'] == True]
office_supplies.groupby('category')['price'].mean()
```

### 3. Price Comparison Tool

Compare prices across stores:

```python
price_comparison = df.groupby('store')['price'].agg(['mean', 'min', 'max'])
print(price_comparison)
```

### 4. Inventory Dashboard

Track availability:

```python
availability = df.groupby('store')['available'].apply(lambda x: (x.sum() / len(x) * 100))
print(f"Store availability rates:\n{availability}")
```

### 5. Category Analysis

```python
category_stats = df.groupby('category').agg({
    'price': ['mean', 'count'],
    'discount_percentage': 'mean',
    'rating': 'mean'
})
print(category_stats)
```

---

## 🚀 Quick Examples

### Open in Excel

```powershell
start stationery_products_20251118_162642.csv
```

### Load in Python

```python
import pandas as pd
import json

# CSV
df = pd.read_csv('stationery_products_20251118_162642.csv')
print(df.head())

# JSON
with open('stationery_products_20251118_162642.json', 'r', encoding='utf-8') as f:
    products = json.load(f)
    print(f"Total: {len(products)}")
```

### Filter by Price Range

```python
# Products under $50
affordable = df[df['price'] <= 50]
print(f"Affordable items: {len(affordable)}")

# Premium products
premium = df[df['price'] >= 200]
print(f"Premium items: {len(premium)}")
```

### Get Products by Category

```python
# Writing instruments
escritura = df[df['category'] == 'Escritura']

# Technology products
tech = df[df['category'] == 'Tecnología y Cómputo']

# Art supplies
arte = df[df['category'] == 'Artículos de Arte']
```

### Find Best Deals

```python
# Products with highest discounts
best_deals = df[df['discount_percentage'] > 20].sort_values('discount_percentage', ascending=False)
print(best_deals[['name', 'price', 'list_price', 'discount_percentage']].head(10))
```

---

## 🏪 Store Distribution

All major Mexican stationery stores represented:

- **Office Depot** - 251 products
- **OfficeMax** - 510 products (combined)
- **Lumen** - 240 products
- **Papelería Cornejo** - 224 products
- **Walmart** - 281 products
- **Costco** - 262 products
- **Amazon México** - 232 products

---

## 📊 Import to Database

### SQLite

```python
import sqlite3
import pandas as pd

df = pd.read_csv('stationery_products_20251118_162642.csv')
conn = sqlite3.connect('stationery.db')
df.to_sql('products', conn, if_exists='replace', index=False)
conn.close()
```

### MySQL

```python
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv('stationery_products_20251118_162642.csv')
engine = create_engine('mysql://user:pass@localhost/stationery_db')
df.to_sql('products', engine, if_exists='replace', index=False)
```

### PostgreSQL

```python
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_csv('stationery_products_20251118_162642.csv')
engine = create_engine('postgresql://user:pass@localhost/stationery_db')
df.to_sql('products', engine, if_exists='replace', index=False)
```

---

## 🔧 Generate More Data

Run the generator again for different datasets:

```powershell
python scripts/generate_stationery_products.py
```

Edit count in the script for more/less products:

```python
products = generate_mexican_stationery_products(count=5000)
```

---

## 💡 Business Insights

### Popular Categories

1. Archivado y Organización (180 products)
2. Tecnología y Cómputo (178 products)
3. Escritorio y Accesorios (174 products)

### Market Segments

- **School Supplies:** 33.2% (664 products) - Perfect for Aug-Sep promotions
- **Office Supplies:** 33.7% (673 products) - Year-round demand
- **Art & Creative:** 8% (161 products) - Hobby and education market

### Pricing Strategy

- Budget items (<$50): 65% of products
- Mid-range ($50-$200): 30% of products
- Premium (>$200): 5% of products

---

## 📈 Analytics Ideas

1. **Seasonal Trends** - Track back-to-school demand
2. **Brand Performance** - Compare brands by rating and sales
3. **Store Comparison** - Analyze pricing strategies
4. **Inventory Optimization** - Predict stock needs
5. **Recommendation Engine** - Suggest related products
6. **Price Alerts** - Notify users of discounts

---

## 🎓 Educational Use

Perfect for:

- Database design projects
- E-commerce platform development
- Data visualization assignments
- Machine learning training
- Business intelligence dashboards
- Inventory management systems

---

## 📞 Next Steps

1. ✅ Open CSV in Excel to explore data
2. ✅ Import to your database
3. ✅ Build queries and reports
4. ✅ Create visualizations
5. ✅ Integrate with n8n workflows
6. ✅ Build your stationery e-commerce platform!

---

**Total Dataset:** 2,000 products | 12 categories | 71 brands | 8 stores
