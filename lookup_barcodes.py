"""
Barcode Lookup and Validation Script
Validates and looks up EAN-13/UPC codes for products in grocery-products.json
"""

import json
import time
import requests
from typing import Dict, List, Optional

def calculate_ean13_check_digit(barcode_12: str) -> str:
    """Calculate EAN-13 check digit from first 12 digits"""
    if len(barcode_12) != 12:
        return None
    
    odd_sum = sum(int(barcode_12[i]) for i in range(0, 12, 2))
    even_sum = sum(int(barcode_12[i]) for i in range(1, 12, 2))
    total = odd_sum + (even_sum * 3)
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def calculate_upc_check_digit(barcode_11: str) -> str:
    """Calculate UPC-A check digit from first 11 digits"""
    if len(barcode_11) != 11:
        return None
    
    odd_sum = sum(int(barcode_11[i]) for i in range(0, 11, 2))
    even_sum = sum(int(barcode_11[i]) for i in range(1, 11, 2))
    total = (odd_sum * 3) + even_sum
    check_digit = (10 - (total % 10)) % 10
    return str(check_digit)

def validate_ean13(ean13: str) -> bool:
    """Validate EAN-13 check digit"""
    if not ean13 or len(ean13) != 13 or not ean13.isdigit():
        return False
    
    calculated = calculate_ean13_check_digit(ean13[:12])
    return calculated == ean13[12]

def validate_upc(upc: str) -> bool:
    """Validate UPC-A check digit"""
    if not upc or len(upc) != 12 or not upc.isdigit():
        return False
    
    calculated = calculate_upc_check_digit(upc[:11])
    return calculated == upc[11]

def lookup_barcode_upcitemdb(barcode: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """
    Look up barcode in UPCitemdb.com API
    Free tier: 100 requests/day without API key
    Get API key at: https://www.upcitemdb.com/api/explorer
    """
    url = f"https://api.upcitemdb.com/prod/trial/lookup"
    params = {"upc": barcode}
    headers = {}
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                return data["items"][0]
        return None
    except Exception as e:
        print(f"Error looking up {barcode}: {e}")
        return None

def lookup_barcode_openfoodfacts(barcode: str) -> Optional[Dict]:
    """
    Look up barcode in Open Food Facts database
    Free API, no rate limits for reasonable use
    Focus on food products
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return data.get("product")
        return None
    except Exception as e:
        print(f"Error looking up {barcode} in Open Food Facts: {e}")
        return None

def process_products(input_file: str, output_file: str, lookup_api: bool = False, api_key: Optional[str] = None):
    """
    Process products and validate/lookup barcodes
    
    Args:
        input_file: Path to grocery-products.json
        output_file: Path to save validation results
        lookup_api: Whether to look up barcodes in external APIs
        api_key: Optional API key for UPCitemdb (if using that service)
    """
    print("Loading products...")
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Processing {len(products)} products...")
    
    results = []
    valid_ean13 = 0
    invalid_ean13 = 0
    valid_upc = 0
    invalid_upc = 0
    found_in_db = 0
    
    for i, product in enumerate(products):
        sku = product.get('sku', 'Unknown')
        upc = product.get('upc', '')
        ean13 = product.get('ean13', '')
        name = product.get('name', '')
        
        # Validate barcodes
        upc_valid = validate_upc(upc)
        ean13_valid = validate_ean13(ean13)
        
        if upc_valid:
            valid_upc += 1
        else:
            invalid_upc += 1
        
        if ean13_valid:
            valid_ean13 += 1
        else:
            invalid_ean13 += 1
        
        result = {
            'sku': sku,
            'name': name,
            'upc': upc,
            'upc_valid': upc_valid,
            'ean13': ean13,
            'ean13_valid': ean13_valid
        }
        
        # Look up in external databases if requested
        if lookup_api and (upc_valid or ean13_valid):
            barcode_to_lookup = ean13 if ean13_valid else upc
            
            # Try Open Food Facts first (free, no limits)
            api_data = lookup_barcode_openfoodfacts(barcode_to_lookup)
            
            if api_data:
                found_in_db += 1
                result['found_in_db'] = True
                result['api_name'] = api_data.get('product_name', '')
                result['api_brand'] = api_data.get('brands', '')
                result['api_categories'] = api_data.get('categories', '')
                print(f"✓ Found {sku}: {name} → {api_data.get('product_name', 'Unknown')}")
            else:
                result['found_in_db'] = False
                print(f"✗ Not found {sku}: {name}")
            
            # Rate limiting - be nice to free APIs
            time.sleep(0.5)
        
        results.append(result)
        
        # Progress update
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(products)} products...")
    
    # Save results
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Total products: {len(products)}")
    print(f"\nUPC-A Validation:")
    print(f"  Valid: {valid_upc} ({valid_upc/len(products)*100:.1f}%)")
    print(f"  Invalid: {invalid_upc} ({invalid_upc/len(products)*100:.1f}%)")
    print(f"\nEAN-13 Validation:")
    print(f"  Valid: {valid_ean13} ({valid_ean13/len(products)*100:.1f}%)")
    print(f"  Invalid: {invalid_ean13} ({invalid_ean13/len(products)*100:.1f}%)")
    
    if lookup_api:
        print(f"\nAPI Lookup:")
        print(f"  Found in database: {found_in_db} ({found_in_db/len(products)*100:.1f}%)")
    
    print(f"\nResults saved to: {output_file}")
    print("="*60)

def extract_upc_list(input_file: str, output_file: str):
    """Extract all UPC codes to a text file, one per line"""
    print(f"Extracting UPC codes from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    upcs = [product.get('upc', '') for product in products if product.get('upc')]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(upcs))
    
    print(f"Extracted {len(upcs)} UPC codes to {output_file}")

def extract_ean13_list(input_file: str, output_file: str):
    """Extract all EAN-13 codes to a text file, one per line"""
    print(f"Extracting EAN-13 codes from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    ean13s = [product.get('ean13', '') for product in products if product.get('ean13')]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ean13s))
    
    print(f"Extracted {len(ean13s)} EAN-13 codes to {output_file}")

if __name__ == "__main__":
    import sys
    
    input_file = "simple-scanner-app/grocery-products.json"
    
    print("Barcode Lookup and Validation Tool")
    print("="*60)
    print("\nOptions:")
    print("1. Validate barcodes only (fast)")
    print("2. Validate + lookup in Open Food Facts API (slow)")
    print("3. Extract UPC codes to text file")
    print("4. Extract EAN-13 codes to text file")
    print("\nEnter option (1-4) or press Enter for option 1: ", end='')
    
    choice = input().strip() or "1"
    
    if choice == "1":
        process_products(
            input_file=input_file,
            output_file="barcode_validation_results.json",
            lookup_api=False
        )
    elif choice == "2":
        print("\nWARNING: This will make API calls for all products.")
        print("Open Food Facts is free but please be respectful of their resources.")
        print("\nContinue? (y/n): ", end='')
        
        if input().strip().lower() == 'y':
            process_products(
                input_file=input_file,
                output_file="barcode_lookup_results.json",
                lookup_api=True
            )
    elif choice == "3":
        extract_upc_list(input_file, "upc_codes.txt")
    elif choice == "4":
        extract_ean13_list(input_file, "ean13_codes.txt")
    else:
        print("Invalid option")
