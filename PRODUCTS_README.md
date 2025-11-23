# Mexico Grocery Products Data Collection

This folder contains tools to collect product data from Mexican grocery stores.

## Available Methods

### 1. Python Script (Recommended for Large Datasets)

Run the Python script to scrape thousands of products:

```powershell
# Install required package
pip install requests

# Run the scraper
python scripts/scrape_grocery_products.py
```

**Features:**

- Scrapes from Soriana (and can be extended to Walmart Mexico, Chedraui, etc.)
- Collects: SKU, name, brand, category, price, list price, availability, images, URLs
- Exports to both JSON and CSV formats
- Includes rate limiting to be respectful to servers
- Can collect 2000+ products

### 2. n8n Workflow

Import the workflow into your n8n instance:

1. Open n8n at http://localhost:5678
2. Go to Workflows → Import from File
3. Select `workflows/mexico-grocery-products-workflow.json`
4. Execute the workflow

**Features:**

- Visual workflow interface
- Automated pagination
- Rate limiting built-in
- Exports to JSON
- Easy to modify and extend

## Data Fields Collected

Each product record includes:

| Field         | Description                         |
| ------------- | ----------------------------------- |
| `sku`         | Product SKU/ID                      |
| `name`        | Product name                        |
| `brand`       | Brand name                          |
| `category`    | Product category                    |
| `price`       | Current selling price (MXN)         |
| `list_price`  | Original/list price (MXN)           |
| `available`   | Stock availability (true/false)     |
| `image_url`   | Product image URL                   |
| `product_url` | Link to product page                |
| `store`       | Store name (Soriana, Walmart, etc.) |
| `description` | Product description                 |
| `scraped_at`  | Timestamp of data collection        |

## Supported Stores

Currently implemented:

- ✅ **Soriana** - Full API access
- 🔄 **Walmart Mexico** - Partial (may require updates)

Can be extended to:

- Chedraui
- La Comer
- HEB Mexico
- Bodega Aurrera
- City Market

## Output Files

The scraper generates timestamped files:

- `mexico_grocery_products_YYYYMMDD_HHMMSS.json` - JSON format
- `mexico_grocery_products_YYYYMMDD_HHMMSS.csv` - CSV format (Excel-compatible)

## Usage Examples

### Quick Start

```powershell
# Navigate to project directory
cd C:\Users\IRWIN\OneDrive\Documentos\n8n

# Run scraper
python scripts/scrape_grocery_products.py
```

### Customize Number of Products

Edit `scrape_grocery_products.py` and modify:

```python
scraper.scrape_soriana(max_products=5000)  # Change to desired amount
```

## Legal & Ethical Considerations

⚠️ **Important:**

- This scraper is for educational and research purposes
- Always check the website's `robots.txt` and Terms of Service
- Implement rate limiting (included in code)
- Don't overload servers with requests
- Consider using official APIs when available
- For commercial use, obtain proper permissions

## Troubleshooting

**No products returned:**

- Check your internet connection
- The store API may have changed (APIs can be updated)
- Check if the website is accessible

**Rate limiting errors:**

- Increase the `time.sleep()` value in the script
- Reduce `max_products` value

**CSV encoding issues:**

- The script uses UTF-8-BOM encoding for Excel compatibility
- Open in Excel or Google Sheets for best results

## Extending the Scraper

To add more stores:

1. Find the store's API endpoint (use browser DevTools → Network tab)
2. Add a new method to the scraper class:

```python
def scrape_new_store(self, max_products=1000):
    # Your implementation here
    pass
```

3. Call it in the `main()` function

## Sample Output

```json
{
  "sku": "00750105535347",
  "name": "Coca-Cola Sabor Original 2 L",
  "brand": "Coca-Cola",
  "category": "Bebidas/Refrescos",
  "price": 35.5,
  "list_price": 42.0,
  "available": true,
  "image_url": "https://...",
  "product_url": "https://www.soriana.com/...",
  "store": "Soriana",
  "scraped_at": "2025-11-18T16:15:00"
}
```

## API Rate Limits

Current settings:

- 1 second delay between requests
- ~50 products per request
- Approximately 1000-2000 products in 5-10 minutes

## Support

For issues or questions:

- Check n8n documentation: https://docs.n8n.io/
- Review store's API documentation
- Check browser console for API endpoints
