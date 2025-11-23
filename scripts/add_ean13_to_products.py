import json
import os

def generate_ean13(sku):
    """Generate EAN-13 code (13 digits) - International standard for Mexico"""
    # Use country code for Mexico (750-759)
    country_code = '750'
    
    # Extract numeric part from SKU
    numeric_sku = ''.join(filter(str.isdigit, str(sku)))
    
    # Create 12-digit code (country + manufacturer + product)
    if len(numeric_sku) < 9:
        numeric_sku = numeric_sku.zfill(9)
    else:
        numeric_sku = numeric_sku[:9]
    
    # Combine country code with SKU
    code_12 = country_code + numeric_sku
    
    # Calculate EAN-13 check digit
    odd_sum = sum(int(code_12[i]) for i in range(1, 12, 2))  # positions 2,4,6,8,10,12
    even_sum = sum(int(code_12[i]) for i in range(0, 12, 2))  # positions 1,3,5,7,9,11
    check_digit = (10 - ((even_sum + odd_sum * 3) % 10)) % 10
    
    return code_12 + str(check_digit)

def generate_upc_from_ean(ean13):
    """Convert EAN-13 to UPC-A if it starts with 0"""
    if ean13.startswith('0'):
        return ean13[1:]
    return ean13[:12]

def validate_upc(upc):
    """Validate and fix UPC-A code (12 digits)"""
    if not upc or len(upc) != 12:
        return None
    
    try:
        # Recalculate check digit
        odd_sum = sum(int(upc[i]) for i in range(0, 11, 2))
        even_sum = sum(int(upc[i]) for i in range(1, 11, 2))
        check_digit = (10 - ((odd_sum * 3 + even_sum) % 10)) % 10
        
        # Return UPC with correct check digit
        return upc[:11] + str(check_digit)
    except:
        return None

def add_ean13_to_products(input_file, output_file=None):
    """Add EAN-13 codes to products JSON file"""
    
    # Read input file
    print(f"Reading products from: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Total products: {len(products)}")
    
    # Process each product
    updated_count = 0
    for product in products:
        sku = product.get('sku', '')
        existing_upc = product.get('upc', '')
        
        # Validate or regenerate UPC
        if existing_upc and len(existing_upc) == 12:
            validated_upc = validate_upc(existing_upc)
            if validated_upc:
                product['upc'] = validated_upc
            else:
                # Generate new UPC from SKU
                numeric_sku = ''.join(filter(str.isdigit, str(sku)))
                if len(numeric_sku) < 11:
                    numeric_sku = numeric_sku.zfill(11)
                else:
                    numeric_sku = numeric_sku[:11]
                odd_sum = sum(int(numeric_sku[i]) for i in range(0, 11, 2))
                even_sum = sum(int(numeric_sku[i]) for i in range(1, 11, 2))
                check_digit = (10 - ((odd_sum * 3 + even_sum) % 10)) % 10
                product['upc'] = numeric_sku + str(check_digit)
        
        # Generate EAN-13
        ean13 = generate_ean13(sku)
        product['ean13'] = ean13
        
        updated_count += 1
        
        if updated_count % 1000 == 0:
            print(f"  Processed {updated_count} products...")
    
    print(f"Added EAN-13 codes to {updated_count} products")
    
    # Write output file
    if output_file is None:
        output_file = input_file.replace('.json', '_with_ean13.json')
    
    print(f"Saving to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    
    print(f"Done! File saved: {output_file}")
    
    # Display sample
    if products:
        sample = products[0]
        print(f"\nSample product:")
        print(f"  Name: {sample['name']}")
        print(f"  SKU: {sample['sku']}")
        print(f"  EAN-13: {sample['ean13']}")
        print(f"  UPC-A: {sample['upc']}")
        print(f"  Price: ${sample['price']} {sample['currency']}")

if __name__ == "__main__":
    # Input file path
    input_file = r"C:\Users\IRWIN\OneDrive\Documentos\n8n\product-scanner-app\src\assets\data\grocery-products.json"
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File not found - {input_file}")
        print("\nPlease provide the correct path to your grocery-products.json file")
        exit(1)
    
    # Output file (overwrite original by default)
    # To create a new file, change output_file to a different path
    output_file = input_file  # Overwrites original
    # output_file = input_file.replace('.json', '_with_ean13.json')  # Creates new file
    
    # Process the file
    add_ean13_to_products(input_file, output_file)
