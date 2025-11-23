import json
import random
from datetime import datetime

def generate_mexican_stationery_products(count=2000):
    """
    Generate realistic Mexican stationery store product data
    Based on popular stores like Office Depot, OfficeMax, Lumen, Papelería Cornejo
    """
    
    products = []
    
    # Realistic Mexican stationery data
    categories_data = {
        'Escritura': {
            'brands': ['Bic', 'Pelikan', 'Paper Mate', 'Pilot', 'Sharpie', 'Pentel', 'Stabilo', 
                      'Faber-Castell', 'Staedtler', 'Uni-ball', 'Reynolds'],
            'products': [
                ('Pluma Azul', '1pz', (5, 12)),
                ('Pluma Negra', '1pz', (5, 12)),
                ('Pluma Roja', '1pz', (5, 12)),
                ('Bolígrafo de Gel', '1pz', (15, 30)),
                ('Marcador Permanente', '1pz', (12, 25)),
                ('Marcador Borrable', '1pz', (18, 35)),
                ('Lápiz No. 2', '12pz', (25, 45)),
                ('Portaminas 0.5mm', '1pz', (20, 40)),
                ('Plumón para Pizarrón', '4pz', (45, 75)),
                ('Resaltador Fluorescente', '4pz', (35, 60)),
                ('Corrector Líquido', '1pz', (15, 28)),
                ('Marcador Permanente', '12pz', (120, 180))
            ]
        },
        'Cuadernos y Libretas': {
            'brands': ['Scribe', 'Norma', 'Loro', 'Oxford', 'Five Star', 'Kiut', 'Great Value', 
                      'Alpha', 'Rhino'],
            'products': [
                ('Cuaderno Profesional 100 Hojas', '1pz', (25, 45)),
                ('Cuaderno Francés 100 Hojas', '1pz', (20, 38)),
                ('Libreta Espiral 80 Hojas', '1pz', (18, 32)),
                ('Cuaderno Universitario 200 Hojas', '1pz', (45, 75)),
                ('Block de Notas', '100 hojas', (30, 55)),
                ('Libreta de Dibujo', '50 hojas', (35, 60)),
                ('Cuaderno de Pasta Dura', '100 hojas', (50, 85)),
                ('Post-it Notes', '100 hojas', (25, 45)),
                ('Libreta Ejecutiva', '1pz', (60, 95)),
                ('Cuaderno Doble Raya', '100 hojas', (22, 40))
            ]
        },
        'Hojas y Papel': {
            'brands': ['HP', 'Xerox', 'Epson', 'Canon', 'Report', 'Great Value', 'Boise'],
            'products': [
                ('Papel Bond Blanco Carta', '500 hojas', (85, 135)),
                ('Papel Bond Blanco Oficio', '500 hojas', (95, 150)),
                ('Papel Fotográfico Brillante', '20 hojas', (75, 120)),
                ('Papel Fotográfico Mate', '20 hojas', (70, 115)),
                ('Papel de Colores', '100 hojas', (45, 75)),
                ('Cartulina Blanca', '10pz', (35, 60)),
                ('Cartulina de Colores', '10pz', (40, 68)),
                ('Papel Kraft', '25 hojas', (30, 55)),
                ('Papel Crepé', '10pz', (25, 45)),
                ('Papel China', '10pz', (20, 38))
            ]
        },
        'Archivado y Organización': {
            'brands': ['Wilson Jones', 'Leitz', 'Esselte', 'Pendaflex', 'Avery', 'Oxford', 
                      'Office Depot', 'Officemax'],
            'products': [
                ('Carpeta de Argollas 1"', '1pz', (35, 65)),
                ('Carpeta de Argollas 2"', '1pz', (45, 80)),
                ('Folder Manila Carta', '100pz', (85, 135)),
                ('Folder de Colores', '25pz', (45, 75)),
                ('Archivero Acordeón 12 Divisiones', '1pz', (75, 125)),
                ('Clasificadores con Broche', '10pz', (35, 60)),
                ('Separadores de Colores', '5pz', (15, 28)),
                ('Portafolio Ejecutivo', '1pz', (125, 220)),
                ('Caja de Archivo Muerto', '1pz', (45, 80)),
                ('Charola Portadocumentos', '1pz', (55, 95))
            ]
        },
        'Adhesivos': {
            'brands': ['Resistol', 'Pritt', 'Kores', '3M', 'Scotch', 'UHU', 'Elmer\'s'],
            'products': [
                ('Pegamento Blanco 250ml', '1pz', (18, 32)),
                ('Pegamento en Barra 40g', '1pz', (15, 28)),
                ('Cinta Adhesiva Transparente', '1pz', (12, 22)),
                ('Cinta Canela', '1pz', (18, 32)),
                ('Silicón Líquido', '250ml', (35, 60)),
                ('Cinta Doble Cara', '1pz', (25, 45)),
                ('Pegamento Instantáneo', '3g', (22, 40)),
                ('Cinta Masking Tape', '1pz', (15, 28)),
                ('Diurex Jumbo', '1pz', (45, 75))
            ]
        },
        'Artículos de Arte': {
            'brands': ['Prismacolor', 'Crayola', 'Faber-Castell', 'Giotto', 'Pelikan', 
                      'Artesco', 'Norma'],
            'products': [
                ('Colores de Madera', '12pz', (35, 65)),
                ('Colores de Madera', '24pz', (65, 110)),
                ('Plumones Lavables', '12pz', (45, 80)),
                ('Acuarelas', '12 colores', (55, 95)),
                ('Temperas', '6 colores', (45, 75)),
                ('Pinceles', '5pz', (35, 65)),
                ('Plastilina', '10 colores', (30, 55)),
                ('Crayones', '24pz', (40, 70)),
                ('Gises de Colores', '12pz', (25, 45)),
                ('Block de Dibujo A4', '40 hojas', (45, 75))
            ]
        },
        'Escritorio y Accesorios': {
            'brands': ['Maped', 'Staples', 'Office Depot', 'Swingline', 'Acco', 'Artline'],
            'products': [
                ('Engrapadora Estándar', '1pz', (45, 85)),
                ('Perforadora 2 Agujeros', '1pz', (55, 95)),
                ('Sacapuntas Metálico', '1pz', (15, 28)),
                ('Tijeras 8"', '1pz', (35, 65)),
                ('Regla 30cm', '1pz', (12, 22)),
                ('Grapas Estándar', '5000pz', (25, 45)),
                ('Clips Mariposa', '100pz', (18, 32)),
                ('Clips Estándar', '100pz', (12, 22)),
                ('Ligas', '100g', (15, 28)),
                ('Organizador de Escritorio', '1pz', (85, 145)),
                ('Porta Clips Magnético', '1pz', (35, 65)),
                ('Despachador de Cinta', '1pz', (45, 80))
            ]
        },
        'Tecnología y Cómputo': {
            'brands': ['HP', 'Logitech', 'Microsoft', 'Kingston', 'SanDisk', 'Verbatim', 
                      'Trust', 'Genius'],
            'products': [
                ('Mouse Inalámbrico', '1pz', (125, 250)),
                ('Teclado USB', '1pz', (145, 280)),
                ('USB 32GB', '1pz', (85, 145)),
                ('USB 64GB', '1pz', (125, 210)),
                ('Cable USB Tipo C', '1m', (55, 95)),
                ('Audífonos con Micrófono', '1pz', (95, 180)),
                ('Webcam HD', '1pz', (350, 650)),
                ('Mouse Pad', '1pz', (35, 65)),
                ('Hub USB 4 Puertos', '1pz', (125, 220)),
                ('Adaptador HDMI', '1pz', (85, 145))
            ]
        },
        'Consumibles de Impresión': {
            'brands': ['HP', 'Canon', 'Epson', 'Brother', 'Samsung', 'Xerox'],
            'products': [
                ('Cartucho Negro Compatible', '1pz', (185, 320)),
                ('Cartucho Color Compatible', '1pz', (210, 380)),
                ('Tóner Negro', '1pz', (450, 850)),
                ('Papel Fotográfico A4', '50 hojas', (125, 210)),
                ('Etiquetas Autoadheribles', '100pz', (45, 85)),
                ('CD-R Grabable', '10pz', (65, 115)),
                ('DVD-R Grabable', '10pz', (75, 125))
            ]
        },
        'Mochilas y Loncheras': {
            'brands': ['Totto', 'JanSport', 'Kipling', 'Nike', 'Adidas', 'Puma', 'Herschel'],
            'products': [
                ('Mochila Escolar Básica', '1pz', (250, 450)),
                ('Mochila con Ruedas', '1pz', (450, 850)),
                ('Mochila Ejecutiva', '1pz', (350, 650)),
                ('Lonchera Térmica', '1pz', (125, 220)),
                ('Estuche Escolar', '1pz', (65, 115)),
                ('Mochila Deportiva', '1pz', (280, 520)),
                ('Bolsa para Laptop 15"', '1pz', (225, 420))
            ]
        },
        'Calculadoras': {
            'brands': ['Casio', 'Texas Instruments', 'HP', 'Canon', 'Sharp', 'Citizen'],
            'products': [
                ('Calculadora Básica', '1pz', (55, 95)),
                ('Calculadora Científica', '1pz', (185, 350)),
                ('Calculadora Financiera', '1pz', (450, 850)),
                ('Calculadora de Escritorio', '1pz', (125, 220)),
                ('Calculadora Impresora', '1pz', (850, 1500))
            ]
        },
        'Pizarrones': {
            'brands': ['Studmark', 'Office Depot', '3M', 'Quartet', 'Artline'],
            'products': [
                ('Pizarrón Blanco 40x60cm', '1pz', (145, 280)),
                ('Pizarrón Blanco 60x90cm', '1pz', (250, 450)),
                ('Pizarrón Corcho 40x60cm', '1pz', (125, 220)),
                ('Borrador para Pizarrón', '1pz', (25, 45)),
                ('Marcadores para Pizarrón', '4pz', (55, 95)),
                ('Chinches de Colores', '100pz', (22, 40))
            ]
        }
    }
    
    stores = ['Office Depot', 'OfficeMax', 'Lumen', 'Office Max', 'Papelería Cornejo', 
              'Walmart', 'Costco', 'Amazon México']
    
    # Generate products
    product_id = 5000000
    
    for i in range(count):
        # Select random category
        category = random.choice(list(categories_data.keys()))
        cat_data = categories_data[category]
        
        # Select random brand and product
        brand = random.choice(cat_data['brands'])
        product_info = random.choice(cat_data['products'])
        
        product_name, size, price_range = product_info
        
        # Calculate prices
        base_price = random.uniform(price_range[0], price_range[1])
        has_discount = random.random() < 0.25  # 25% of products have discount
        
        if has_discount:
            discount = random.uniform(0.10, 0.35)
            list_price = round(base_price / (1 - discount), 2)
            current_price = round(base_price, 2)
        else:
            list_price = round(base_price, 2)
            current_price = round(base_price, 2)
        
        # Generate product
        product = {
            'sku': f"ST{product_id + i}",
            'upc': f"750{random.randint(100000000, 999999999)}",
            'name': f"{brand} {product_name} {size}",
            'brand': brand,
            'category': category,
            'subcategory': product_name,
            'size': size,
            'price': current_price,
            'list_price': list_price,
            'discount_percentage': round(((list_price - current_price) / list_price * 100), 1) if has_discount else 0,
            'currency': 'MXN',
            'available': random.choice([True] * 9 + [False]),  # 90% available
            'stock_quantity': random.randint(0, 200) if random.choice([True] * 9 + [False]) else 0,
            'image_url': f"https://cdn.stationery-store.mx/products/{product_id + i}.jpg",
            'product_url': f"https://www.{random.choice(stores).lower().replace(' ', '')}.com.mx/producto/{product_id + i}",
            'store': random.choice(stores),
            'description': f"{brand} {product_name} {size} - Artículo de papelería de alta calidad",
            'rating': round(random.uniform(3.8, 5.0), 1),
            'reviews_count': random.randint(0, 300),
            'is_school_supply': category in ['Escritura', 'Cuadernos y Libretas', 'Artículos de Arte', 'Mochilas y Loncheras'],
            'is_office_supply': category in ['Archivado y Organización', 'Escritorio y Accesorios', 'Hojas y Papel', 'Calculadoras'],
            'scraped_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        products.append(product)
    
    return products


def save_products(products, format='both'):
    """Save products to JSON and/or CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format in ['json', 'both']:
        filename = f'stationery_products_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved to {filename}")
    
    if format in ['csv', 'both']:
        import csv
        filename = f'stationery_products_{timestamp}.csv'
        
        if products:
            keys = products[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(products)
            print(f"✅ Saved to {filename}")


def print_summary(products):
    """Print summary statistics"""
    print("\n" + "="*70)
    print("STATIONERY PRODUCTS DATASET SUMMARY")
    print("="*70)
    
    print(f"\n📦 Total Products: {len(products)}")
    
    # By store
    stores = {}
    for p in products:
        store = p['store']
        stores[store] = stores.get(store, 0) + 1
    
    print("\n🏪 Products by Store:")
    for store, count in sorted(stores.items(), key=lambda x: x[1], reverse=True):
        print(f"   {store}: {count}")
    
    # By category
    categories = {}
    for p in products:
        cat = p['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📂 Products by Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   {cat}: {count}")
    
    # Brands
    brands = set(p['brand'] for p in products)
    print(f"\n🏷️  Unique Brands: {len(brands)}")
    
    # School vs Office supplies
    school = sum(1 for p in products if p['is_school_supply'])
    office = sum(1 for p in products if p['is_office_supply'])
    print(f"\n📚 School Supplies: {school} ({school/len(products)*100:.1f}%)")
    print(f"💼 Office Supplies: {office} ({office/len(products)*100:.1f}%)")
    
    # Availability
    available = sum(1 for p in products if p['available'])
    print(f"\n✅ Available Products: {available} ({available/len(products)*100:.1f}%)")
    
    # Price stats
    prices = [p['price'] for p in products]
    print(f"\n💰 Price Range:")
    print(f"   Min: ${min(prices):.2f} MXN")
    print(f"   Max: ${max(prices):.2f} MXN")
    print(f"   Average: ${sum(prices)/len(prices):.2f} MXN")
    
    # Discounts
    discounted = sum(1 for p in products if p['discount_percentage'] > 0)
    print(f"\n🎯 Products with Discount: {discounted} ({discounted/len(products)*100:.1f}%)")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    print("="*70)
    print("MEXICO STATIONERY PRODUCTS - SAMPLE DATA GENERATOR")
    print("="*70)
    print("\nGenerating realistic Mexican stationery store product dataset...")
    print("This creates a comprehensive dataset with realistic brands, prices,")
    print("and product information from major Mexican stationery stores.\n")
    
    # Generate products
    products = generate_mexican_stationery_products(count=2000)
    
    # Print summary
    print_summary(products)
    
    # Save to files
    print("\n💾 Saving files...")
    save_products(products, format='both')
    
    print("\n" + "="*70)
    print("✨ GENERATION COMPLETED!")
    print("="*70)
    print("\nYou now have a comprehensive dataset of Mexican stationery products!")
    print("Perfect for:")
    print("  • Testing e-commerce applications")
    print("  • Back-to-school shopping platforms")
    print("  • Office supply management systems")
    print("  • Price comparison tools")
    print("  • Data analysis and visualization")
    print("  • Inventory management systems")
    print("="*70)
