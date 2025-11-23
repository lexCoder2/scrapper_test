# Barcode Fields Summary

## Overview

All three store scrapers have been updated to extract all available barcode and identification fields from their APIs and store them in MongoDB.

## Extracted Fields by Store

### Chedraui (VTEX)

**New fields added:**

- `multi_ean` - From `MultiEan` field in API (array, first element extracted)
- `ean` - From items[0].ean (item-level EAN)
- `reference` - From items[0].referenceId[0].Value
- `product_id` - Product ID from API

**Example data:**

```json
{
  "sku": "3733641",
  "ean13": "17501055374752",
  "upc": "373364100009",
  "ean": "17501055374752",
  "multi_ean": "7501055374755",
  "reference": "3733641",
  "product_id": "3733641"
}
```

### La Comer (Amarello)

**New fields added:**

- `art_ean` - From `artEan` field (primary barcode from store)
- `art_cod` - From `artCod` (product code)

**Example data:**

```json
{
  "sku": "78979116",
  "ean13": "735257004005",
  "upc": "789791160002",
  "art_ean": "735257004005",
  "art_cod": "78979116"
}
```

### Papelerias Tony (VTEX)

**New fields added:**

- `item_ean` - From items[0].ean (item-level EAN)
- `product_reference` - From `productReference` field
- `product_reference_code` - From `productReferenceCode` field

**Example data:**

```json
{
  "sku": "4335",
  "ean13": "17501147457615",
  "upc": "043350000027",
  "item_ean": "17501147457615",
  "product_reference": "08330011",
  "product_reference_code": "08330011"
}
```

## Changes Made

### 1. Removed Product Limits

- Removed `max_per_store = 100` limitation
- Removed all `if store_count >= max_per_store: break` conditions
- Changed progress display from `X/100` to `X products` with updates every 100 products
- Each store now scrapes ALL available products

### 2. Expanded Categories

**Chedraui:** Added 15 categories (was 5)

- Bebidas, Despensa, Lácteos y Huevo, Limpieza del Hogar
- Cuidado Personal, Salchichonería, Refrigerado y Congelado
- Carnes/Pescados/Mariscos, Panadería y Tortillería
- Frutas y Verduras, Quesos, Productos a Granel
- Desechables, Botanas y Dulces, Café y Sustitutos

**La Comer:** Expanded from 10 to 30 search terms

- Added: congelados, refrigerados, salchichoneria, quesos, cereales
- enlatados, pastas, arroz, aceites, salsas, condimentos
- dulces, chocolates, galletas, cafe, te, jugos, refrescos
- agua, vinos, cervezas, licores, snacks, papas, semillas

**Papelerias Tony:** Expanded from 23 to 43 search terms

- Added: crayones, acuarelas, temperas, plumon, resaltador, corrector
- goma, cinta adhesiva, hojas, cartulina, foami, diamantina
- silicones, pistola, plastilina, porcelana, lienzo, caballete
- estuche, lonchera, lapicera, agenda, libreta, block
- folder, mica, broche, perforadora, sello, almohadilla, etiqueta, separadores

### 3. Optimized Performance

- Reduced sleep time from 0.5-1.5s to 0.3-0.8s between requests
- Increased pagination limits (Chedraui: 20→100 pages, La Comer: 25→100 pages, Tony: 5→20 pages)

## Database Schema Updates

All products now include these barcode fields where available:

```javascript
{
  // Core fields (all stores)
  sku: String,
  ean13: String,
  upc: String,

  // Chedraui-specific
  ean: String,
  multi_ean: String,
  reference: String,
  product_id: String,

  // La Comer-specific
  art_ean: String,
  art_cod: String,

  // Papelerias Tony-specific
  item_ean: String,
  product_reference: String,
  product_reference_code: String,

  // ... other product fields
}
```

## Expected Results

### Product Count Estimates

- **Chedraui:** ~50,000+ products (15 categories × 100 pages × 50 products)
- **La Comer:** ~120,000+ products (30 terms × 100 pages × 40 products)
- **Papelerias Tony:** ~43,000+ products (43 terms × 20 pages × 50 products)

**Total expected:** 200,000+ products

## Usage

Run the updated scraper:

```bash
python scrape_all_stores.py
```

The scraper will now:

1. Collect ALL products from each store (no 100-product limit)
2. Extract and store all available barcode fields
3. Display progress every 100 products
4. Save everything to MongoDB with enhanced barcode data
