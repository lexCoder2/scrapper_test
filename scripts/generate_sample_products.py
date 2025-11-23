import json
import random
from datetime import datetime

def generate_mexican_grocery_products(count=2000):
    """
    Generate realistic Mexican grocery store product data
    Perfect for testing, demos, or when live scraping isn't available
    """
    
    products = []
    
    # Realistic Mexican grocery data
    categories_data = {
        'Bebidas': {
            'brands': ['Coca-Cola', 'Pepsi', 'Boing', 'Jumex', 'Del Valle', 'Bonafont', 'Ciel', 
                      'Electrolit', 'Peñafiel', 'Jarritos', 'Sangría Señorial', 'Mundet'],
            'products': [
                ('Refresco Cola', '2L', (30, 45)),
                ('Refresco Cola', '600ml', (15, 22)),
                ('Agua Natural', '1.5L', (12, 20)),
                ('Agua Natural', '600ml', (8, 12)),
                ('Jugo de Naranja', '1L', (25, 38)),
                ('Jugo de Mango', '1L', (25, 38)),
                ('Bebida Deportiva', '500ml', (18, 28)),
                ('Agua Mineral', '600ml', (15, 23)),
                ('Refresco de Manzana', '355ml', (12, 18)),
                ('Refresco de Jamaica', '355ml', (12, 18)),
                ('Té Verde', '1L', (20, 30)),
                ('Té Negro', '1L', (20, 30))
            ]
        },
        'Lácteos': {
            'brands': ['Lala', 'Alpura', 'Santa Clara', 'Nestlé', 'Philadelphia', 'Danone', 
                      'Yakult', 'Fud', 'Yoplait', 'Chambourcy'],
            'products': [
                ('Leche Entera', '1L', (22, 32)),
                ('Leche Deslactosada', '1L', (25, 35)),
                ('Yogurt Natural', '1kg', (35, 50)),
                ('Yogurt con Fruta', '150g', (10, 15)),
                ('Queso Panela', '400g', (45, 65)),
                ('Queso Oaxaca', '400g', (50, 70)),
                ('Crema Ácida', '200ml', (18, 28)),
                ('Mantequilla', '90g', (22, 32)),
                ('Queso Crema', '190g', (30, 45)),
                ('Yogurt Bebible', '240ml', (12, 18))
            ]
        },
        'Despensa': {
            'brands': ['La Costeña', 'Herdez', 'Barilla', 'Maseca', 'Verde Valle', 'McCormick', 
                      'Knorr', 'Búfalo', 'Del Fuerte', 'Isadora', 'Clemente Jacques'],
            'products': [
                ('Frijoles Negros', '580g', (18, 28)),
                ('Frijoles Bayos', '580g', (18, 28)),
                ('Arroz Blanco', '1kg', (25, 38)),
                ('Aceite Vegetal', '1L', (35, 55)),
                ('Pasta Espagueti', '200g', (12, 20)),
                ('Atún en Agua', '140g', (15, 23)),
                ('Salsa Verde', '210g', (12, 20)),
                ('Salsa Roja', '210g', (12, 20)),
                ('Harina de Trigo', '1kg', (18, 28)),
                ('Harina de Maíz', '1kg', (20, 30)),
                ('Chiles Jalapeños', '220g', (15, 25)),
                ('Mayonesa', '385g', (28, 42))
            ]
        },
        'Carnes y Embutidos': {
            'brands': ['FUD', 'San Rafael', 'Zwan', 'KIR', 'Chimex', 'Campofrio', 'Oscar Mayer'],
            'products': [
                ('Jamón de Pavo', '200g', (45, 70)),
                ('Salchicha de Pavo', '500g', (55, 80)),
                ('Tocino', '180g', (48, 72)),
                ('Chorizo', '400g', (52, 78)),
                ('Salami', '200g', (42, 65)),
                ('Pechuga de Pavo', '250g', (65, 95)),
                ('Mortadela', '250g', (35, 55))
            ]
        },
        'Panadería': {
            'brands': ['Bimbo', 'Marinela', 'Suandy', 'Wonder', 'Tía Rosa', 'Oroweat'],
            'products': [
                ('Pan de Caja Blanco', '680g', (38, 52)),
                ('Pan de Caja Integral', '680g', (42, 58)),
                ('Pan Tostado', '270g', (32, 48)),
                ('Panqué', '250g', (28, 42)),
                ('Donas', '105g', (18, 28)),
                ('Roles de Canela', '230g', (32, 48))
            ]
        },
        'Botanas y Snacks': {
            'brands': ['Sabritas', 'Barcel', 'Gamesa', 'Marinela', 'Ricolino', 'Carlos V', 
                      'Totis', 'Takis', 'Cheetos'],
            'products': [
                ('Papas Fritas Naturales', '45g', (12, 18)),
                ('Papas Fritas Naturales', '170g', (32, 48)),
                ('Papas Fritas con Chile', '62g', (15, 22)),
                ('Galletas Saladas', '200g', (18, 28)),
                ('Galletas Marías', '200g', (15, 25)),
                ('Galletas de Chocolate', '120g', (18, 28)),
                ('Chocolate', '40g', (12, 18)),
                ('Chicles', '12pz', (10, 15)),
                ('Paletas de Caramelo', '30g', (8, 12)),
                ('Cacahuates Japoneses', '80g', (15, 22))
            ]
        },
        'Limpieza': {
            'brands': ['Fabuloso', 'Pinol', 'Ajax', 'Cloralex', 'Suavitel', 'Ariel', 'Ace', 
                      'Salvo', 'Maestro Limpio', 'Zote'],
            'products': [
                ('Limpiador Multiusos Lavanda', '1L', (28, 42)),
                ('Limpiador Multiusos Limón', '1L', (28, 42)),
                ('Cloro', '1L', (18, 28)),
                ('Jabón Líquido para Trastes', '500ml', (22, 35)),
                ('Suavizante de Ropa', '1L', (32, 48)),
                ('Detergente en Polvo', '1kg', (45, 68)),
                ('Detergente Líquido', '1L', (55, 82)),
                ('Jabón para Ropa en Barra', '450g', (22, 35)),
                ('Limpiador de Pisos', '1L', (25, 38))
            ]
        },
        'Higiene Personal': {
            'brands': ['Palmolive', 'Colgate', 'Gillette', 'Head & Shoulders', 'Dove', 'Axe', 
                      'Pantene', 'Sedal', 'Suave', 'Garnier', 'Nivea'],
            'products': [
                ('Pasta Dental', '75ml', (28, 42)),
                ('Jabón de Tocador', '3pk x 90g', (35, 52)),
                ('Shampoo', '400ml', (48, 72)),
                ('Acondicionador', '400ml', (48, 72)),
                ('Desodorante', '50g', (38, 58)),
                ('Papel Higiénico', '4 rollos', (32, 48)),
                ('Toallas Sanitarias', '10pz', (28, 42)),
                ('Rastrillos Desechables', '4pz', (38, 58)),
                ('Gel para Cabello', '250ml', (42, 65))
            ]
        },
        'Cereales': {
            'brands': ['Kelloggs', 'Nestlé', 'Quaker', 'All-Bran', 'Zucaritas'],
            'products': [
                ('Corn Flakes', '500g', (55, 82)),
                ('Hojuelas de Avena', '400g', (45, 68)),
                ('Cereal de Chocolate', '350g', (58, 88)),
                ('Cereal con Miel', '350g', (58, 88)),
                ('Granola', '300g', (65, 95)),
                ('Avena Instantánea', '350g', (42, 62))
            ]
        },
        'Congelados': {
            'brands': ['Holanda', 'Aurrera', 'McCormick', 'Delimex'],
            'products': [
                ('Pizza Congelada', '400g', (75, 110)),
                ('Verduras Mixtas', '500g', (35, 55)),
                ('Papas a la Francesa', '1kg', (48, 72)),
                ('Pollo Empanizado', '450g', (95, 140)),
                ('Helado', '1L', (65, 95))
            ]
        }
    }
    
    stores = ['Soriana', 'Walmart', 'Chedraui', 'Bodega Aurrera', 'HEB', 'Comercial Mexicana', 'La Comer']
    
    # Generate products
    product_id = 1000000
    
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
        has_discount = random.random() < 0.3  # 30% of products have discount
        
        if has_discount:
            discount = random.uniform(0.05, 0.25)
            list_price = round(base_price / (1 - discount), 2)
            current_price = round(base_price, 2)
        else:
            list_price = round(base_price, 2)
            current_price = round(base_price, 2)
        
        # Generate product
        product = {
            'sku': f"MX{product_id + i}",
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
            'stock_quantity': random.randint(0, 500) if random.choice([True] * 9 + [False]) else 0,
            'image_url': f"https://cdn.grocery-store.mx/products/{product_id + i}.jpg",
            'product_url': f"https://www.{random.choice(stores).lower().replace(' ', '')}.com.mx/producto/{product_id + i}",
            'store': random.choice(stores),
            'description': f"{brand} {product_name} {size} - Producto de alta calidad para tu hogar",
            'unit_price': round(current_price, 2),
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews_count': random.randint(0, 500),
            'scraped_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        products.append(product)
    
    return products


def save_products(products, format='both'):
    """Save products to JSON and/or CSV"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format in ['json', 'both']:
        filename = f'mexico_grocery_sample_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved to {filename}")
    
    if format in ['csv', 'both']:
        import csv
        filename = f'mexico_grocery_sample_{timestamp}.csv'
        
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
    print("PRODUCT DATASET SUMMARY")
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
    print("MEXICO GROCERY PRODUCTS - SAMPLE DATA GENERATOR")
    print("="*70)
    print("\nGenerating realistic Mexican grocery store product dataset...")
    print("This creates a comprehensive dataset with realistic brands, prices,")
    print("and product information from major Mexican grocery chains.\n")
    
    # Generate products
    products = generate_mexican_grocery_products(count=2000)
    
    # Print summary
    print_summary(products)
    
    # Save to files
    print("\n💾 Saving files...")
    save_products(products, format='both')
    
    print("\n" + "="*70)
    print("✨ GENERATION COMPLETED!")
    print("="*70)
    print("\nYou now have a comprehensive dataset of Mexican grocery products!")
    print("Perfect for:")
    print("  • Testing e-commerce applications")
    print("  • Price comparison tools")
    print("  • Data analysis and visualization")
    print("  • Machine learning training data")
    print("  • Database population")
    print("="*70)
