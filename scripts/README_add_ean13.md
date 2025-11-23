# Add EAN-13 Codes to Products

This script adds EAN-13 barcodes to existing product JSON files.

## What it does

- Reads a JSON file containing product data
- Generates valid EAN-13 codes (13 digits) for each product using Mexican country code (750)
- Validates and fixes existing UPC-A codes (12 digits)
- Saves the updated data back to the file

## EAN-13 Format

EAN-13 is the international standard barcode format used worldwide:

- **Structure**: 13 digits total
- **Format**: `[Country Code (3)] + [Manufacturer Code (4)] + [Product Code (5)] + [Check Digit (1)]`
- **Mexico**: Country codes 750-759
- **Example**: `7500031028767`

## UPC-A Format

UPC-A is primarily used in North America:

- **Structure**: 12 digits total
- **Format**: `[Number System (1)] + [Manufacturer Code (5)] + [Product Code (5)] + [Check Digit (1)]`
- **Example**: `000031028769`

## Usage

```bash
python add_ean13_to_products.py
```

The script is configured to process:

```
C:\Users\IRWIN\OneDrive\Documentos\n8n\product-scanner-app\src\assets\data\grocery-products.json
```

## Configuration

Edit the script to change input/output files:

```python
# Input file
input_file = r"path\to\your\grocery-products.json"

# Option 1: Overwrite original file
output_file = input_file

# Option 2: Create new file with suffix
output_file = input_file.replace('.json', '_with_ean13.json')
```

## Output

The script will:

1. Process all products (shows progress every 1000 products)
2. Add `ean13` field to each product
3. Validate/fix existing `upc` codes
4. Display a sample product with codes
5. Save the updated JSON file

## Example Output

```
Reading products from: grocery-products.json
Total products: 12300
  Processed 1000 products...
  Processed 2000 products...
  ...
Added EAN-13 codes to 12300 products
Saving to: grocery-products.json
Done! File saved: grocery-products.json

Sample product:
  Name: Zanahoria por kg
  SKU: 3102876
  EAN-13: 7500031028767
  UPC-A: 000031028769
  Price: $13.9 MXN
```

## Product Structure

Each product will have these barcode fields:

```json
{
  "sku": "3102876",
  "ean13": "7500031028767",
  "upc": "000031028769",
  "name": "Zanahoria por kg",
  ...
}
```

## Validation

The script includes:

- ✅ Check digit validation for EAN-13
- ✅ Check digit validation for UPC-A
- ✅ Automatic correction of invalid codes
- ✅ Consistent code generation from SKU

## Notes

- The script uses Mexican country code (750) for EAN-13 generation
- Check digits are calculated using the EAN-13 and UPC-A algorithms
- Existing codes are validated and corrected if needed
- The file is saved with proper UTF-8 encoding and indentation
