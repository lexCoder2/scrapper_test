"""
Multi-Store Product Scraper for Mexican Grocery Stores
Supports: Chedraui, Soriana, La Comer, Bodega Aurrera, Papelerias Tony
"""

import requests
import json
import time
from datetime import datetime
import random
import os
import sys
from urllib.parse import urlparse
import base64
from pymongo import MongoClient, UpdateOne
from pathlib import Path

# Load environment variables from .env file in project root
try:
    from dotenv import load_dotenv
    # Get the project root (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, will use system environment variables only
    pass

class TeeOutput:
    """Write to both console and file"""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')
    
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    
    def flush(self):
        self.terminal.flush()
        self.log.flush()
    
    def close(self):
        self.log.close()

class MultiStoreScraper:
    def __init__(self, mongodb_uri=None, save_images=True, debug_raw=False):
        self.products = []
        self.seen_skus = set()
        self.save_images = save_images
        self.debug_raw = debug_raw
        self.raw_printed = {}  # Track which stores have printed raw data
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        self.images_dir = 'product_images'
        os.makedirs(self.images_dir, exist_ok=True)
        self.placeholder = os.path.join(self.images_dir, 'placeholder.png')
        self._ensure_placeholder()
        
        # MongoDB connection
        self.mongodb_uri = mongodb_uri
        self.db = None
        self.collection = None
        if mongodb_uri:
            self.connect_db()
    
    def connect_db(self):
        """Connect to MongoDB"""
        try:
            client = MongoClient(self.mongodb_uri)
            self.db = client['products']
            self.collection = self.db['grocery_products']
            print("[OK] Connected to MongoDB")
        except Exception as e:
            print(f"[ERROR] MongoDB connection failed: {e}")
            self.collection = None
    
    def generate_upc(self, sku):
        """Generate UPC-A code"""
        numeric_sku = ''.join(filter(str.isdigit, str(sku)))
        if len(numeric_sku) < 11:
            numeric_sku = numeric_sku.zfill(11)
        else:
            numeric_sku = numeric_sku[:11]
        odd_sum = sum(int(numeric_sku[i]) for i in range(0, 11, 2))
        even_sum = sum(int(numeric_sku[i]) for i in range(1, 11, 2))
        check_digit = (10 - ((odd_sum * 3 + even_sum) % 10)) % 10
        return numeric_sku + str(check_digit)
    
    def generate_ean13(self, sku):
        """Generate EAN-13 code"""
        country_code = '750'
        numeric_sku = ''.join(filter(str.isdigit, str(sku)))
        
        if len(numeric_sku) < 9:
            numeric_sku = numeric_sku.zfill(9)
        else:
            numeric_sku = numeric_sku[:9]
        
        code_12 = country_code + numeric_sku
        odd_sum = sum(int(code_12[i]) for i in range(1, 12, 2))
        even_sum = sum(int(code_12[i]) for i in range(0, 12, 2))
        check_digit = (10 - ((even_sum + odd_sum * 3) % 10)) % 10
        
        return code_12 + str(check_digit)
    
    def download_image(self, image_url, sku):
        """Download product image"""
        # Always return a local path. If saving images is disabled or download fails,
        # return the placeholder image path so we don't store remote URLs.
        try:
            if not image_url:
                return self.placeholder

            if image_url.startswith('//'):
                image_url = 'https:' + image_url

            ext = os.path.splitext(urlparse(image_url).path)[1] or '.jpg'
            filename = f"{sku}{ext}"
            filepath = os.path.join(self.images_dir, filename)

            # Check if image already exists locally (even if save_images is disabled)
            if os.path.exists(filepath):
                return filepath

            # If save_images is disabled, don't download new images
            if not self.save_images:
                return self.placeholder

            response = requests.get(image_url, headers=self.headers, timeout=5, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return filepath

        except Exception:
            pass

        return self.placeholder

    def _ensure_placeholder(self):
        """Create a tiny 1x1 PNG placeholder if it doesn't exist."""
        try:
            if os.path.exists(self.placeholder):
                return
            # 1x1 PNG (transparent)
            png_b64 = (
                'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAA'
            )
            with open(self.placeholder, 'wb') as ph:
                ph.write(base64.b64decode(png_b64))
        except Exception:
            # If placeholder creation fails, ensure at least the images_dir exists.
            os.makedirs(self.images_dir, exist_ok=True)
    
    def is_unique_product(self, ean):
        """Check if product is unique (not in memory or DB)"""
        if not ean or ean in self.seen_skus:
            return False
        
        if self.collection is not None:
            existing = self.collection.find_one({'ean': ean})
            if existing:
                return False
        
        self.seen_skus.add(ean)
        return True
    
    def save_product(self, product):
        """Save product to memory and optionally to DB"""
        self.products.append(product)
        
        if self.collection is not None:
            try:
                self.collection.update_one(
                    {'ean': product['ean']},
                    {'$set': product},
                    upsert=True
                )
            except Exception as e:
                print(f"  Error saving to DB: {str(e)[:50]}")
    
    def scrape_chedraui(self):
        """Scrape Chedraui (VTEX platform)"""
        
        initial_count = len(self.products)
        store_count = 0
        
        # All main Chedraui categories
        category_ids = [
            '1/115/',  # Bebidas
            '1/103/',  # Despensa
            '1/10/',   # Lácteos y Huevo
            '1/104/',  # Limpieza del Hogar
            '1/105/',  # Cuidado Personal
            '1/11/',   # Salchichonería
            '1/12/',   # Refrigerado y Congelado
            '1/13/',   # Carnes, Pescados y Mariscos
            '1/14/',   # Panadería y Tortillería
            '1/15/',   # Frutas y Verduras
            '1/16/',   # Quesos
            '1/17/',   # Productos a Granel
            '1/18/',   # Desechables
            '1/19/',   # Botanas y Dulces
            '1/20/',   # Café y Sustitutos
        ]
        
        for category_id in category_ids:
            for page in range(3000):  # Increased pages to get all products
                    
                try:
                    url = f"https://www.chedraui.com.mx/api/catalog_system/pub/products/search"
                    params = {
                        'fq': f'C:/{category_id}',
                        '_from': page * 50,
                        '_to': page * 50 + 49,
                        'O': 'OrderByTopSaleDESC'
                    }
                    
                    response = requests.get(url, params=params, headers=self.headers, timeout=10)
                    
                    if response.status_code not in [200, 206]:
                        break
                    
                    data = response.json()
                    if not data:
                        break
                    
                    for item in data:
                        sku = str(item.get('productId', ''))
                        
                        items = item.get('items', [])
                        first_item = items[0] if items else {}
                        
                        # Collect all possible codes
                        api_ean = first_item.get('ean', '')
                        reference_id = first_item.get('referenceId', [{}])
                        ref_code = reference_id[0].get('Value', '') if reference_id else ''
                        multi_ean = item.get('MultiEan', [''])[0] if item.get('MultiEan') else ''
                        
                        # Determine EAN13 and UPC
                        if api_ean and len(str(api_ean)) == 13:
                            ean13 = str(api_ean)
                            upc = self.generate_upc(sku)
                        elif api_ean and len(str(api_ean)) == 12:
                            upc = str(api_ean)
                            ean13 = '0' + str(api_ean)
                        else:
                            ean13 = self.generate_ean13(sku)
                            upc = self.generate_upc(sku)
                        
                        # Use EAN13 as the primary identifier
                        if not self.is_unique_product(ean13):
                            continue
                        
                        # Store all codes
                        codes = {
                            'sku': sku,
                            'ean': ean13,
                            'multi_ean': str(multi_ean) if multi_ean else '',
                            'upc': upc,
                            'ean13': ean13,
                            'reference': str(ref_code) if ref_code else '',
                            'product_id': str(item.get('productId', ''))
                        }
                        
                        commercial_offer = {}
                        if items:
                            sellers = items[0].get('sellers', [])
                            if sellers:
                                commercial_offer = sellers[0].get('commertialOffer', {})
                        
                        price = commercial_offer.get('Price', 0)
                        list_price = commercial_offer.get('ListPrice', price)
                        
                        image_url = ''
                        if items:
                            images = items[0].get('images', [])
                            if images:
                                image_url = images[0].get('imageUrl', '')
                        
                        # Always resolve to a local path (real image or placeholder)
                        local_image = self.download_image(image_url, codes['ean'])
                        
                        product = {
                            'sku': sku,
                            'ean13': codes['ean13'],
                            'upc': codes['upc'],
                            'ean': codes['ean'],
                            'multi_ean': codes['multi_ean'],
                            'reference': codes['reference'],
                            'product_id': codes['product_id'],
                            'name': item.get('productName', ''),
                            'brand': item.get('brand', 'Sin Marca'),
                            'category': item.get('categories', [''])[0].split('/')[-2] if item.get('categories') else 'Supermercado',
                            'price': float(price) if price else 0.0,
                            'list_price': float(list_price) if list_price else float(price) if price else 0.0,
                            'currency': 'MXN',
                            'available': commercial_offer.get('IsAvailable', True),
                            'stock': commercial_offer.get('AvailableQuantity', 100),
                            'image_url': '',
                            'local_image': local_image,
                            'product_url': f"https://www.chedraui.com.mx{item.get('link', '')}",
                            'store': 'Chedraui',
                            'description': item.get('description', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.save_product(product)
                        store_count += 1
                        if store_count % 100 == 0:
                            print(f"\rChedraui: {store_count} products", end='', flush=True)
                    
                    time.sleep(random.uniform(0.4, 0.9))
                    
                except Exception as e:
                    continue
        
        added = len(self.products) - initial_count
        return added
    
    def scrape_soriana(self):
        """Scrape Soriana (VTEX platform)"""
        print("\n" + "="*60)
        print("SCRAPING SORIANA")
        print("="*60)
        
        initial_count = len(self.products)
        
        # Soriana uses different API structure - try direct category browsing
        categories = [
            'abarrotes', 'bebidas', 'lacteos', 'carnes-y-pescados', 'frutas-y-verduras',
            'panaderia', 'limpieza', 'cuidado-personal', 'mascotas', 'bebe'
        ]
        
        for category in categories:
            for page in range(50):  # Try 50 pages per category
                try:
                    url = f"https://www.soriana.com/{category}"
                    params = {'_from': page * 50, '_to': page * 50 + 49}
                    
                    # Try VTEX API endpoint
                    api_url = f"https://www.soriana.com/api/catalog_system/pub/products/search"
                    api_params = {
                        'fq': f'C:/{category}/',
                        '_from': page * 50,
                        '_to': page * 50 + 49
                    }
                    
                    response = requests.get(api_url, params=api_params, headers=self.headers, timeout=10)
                    
                    if response.status_code not in [200, 206]:
                        break
                    
                    data = response.json()
                    if not data:
                        break
                    
                    # Print raw data for first product from this store
                    if self.debug_raw and 'Soriana' not in self.raw_printed and data:
                        print("\n" + "="*60)
                        print("RAW SOURCE DATA - SORIANA (First Product)")
                        print("="*60)
                        print(json.dumps(data[0], indent=2, ensure_ascii=False))
                        print("="*60 + "\n")
                        self.raw_printed['Soriana'] = True
                    
                    for item in data:
                        sku = str(item.get('productId', ''))
                        
                        items = item.get('items', [])
                        first_item = items[0] if items else {}
                        
                        api_ean = first_item.get('ean', '')
                        if api_ean and len(str(api_ean)) == 13:
                            ean13 = str(api_ean)
                            upc = self.generate_upc(sku)
                        else:
                            ean13 = self.generate_ean13(sku)
                            upc = self.generate_upc(sku)
                        
                        # Use EAN13 as the primary identifier
                        if not self.is_unique_product(ean13):
                            continue
                        
                        commercial_offer = {}
                        if items:
                            sellers = items[0].get('sellers', [])
                            if sellers:
                                commercial_offer = sellers[0].get('commertialOffer', {})
                        
                        price = commercial_offer.get('Price', 0)
                        image_url = ''
                        if items:
                            images = items[0].get('images', [])
                            if images:
                                image_url = images[0].get('imageUrl', '')
                        
                        local_image = self.download_image(image_url, ean13)
                        
                        product = {
                            'sku': sku,
                            'ean': ean13,
                            'upc': upc,
                            'name': item.get('productName', ''),
                            'brand': item.get('brand', 'Sin Marca'),
                            'category': category.replace('-', ' ').title(),
                            'price': float(price) if price else 0.0,
                            'list_price': float(price) if price else 0.0,
                            'currency': 'MXN',
                            'available': True,
                            'stock': 100,
                            'image_url': '',
                            'local_image': local_image,
                            'product_url': f"https://www.soriana.com{item.get('link', '')}",
                            'store': 'Soriana',
                            'description': item.get('description', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.save_product(product)
                    
                    time.sleep(random.uniform(0.5, 1.0))
                    
                except Exception as e:
                    continue
        
        added = len(self.products) - initial_count
        print(f"[OK] Soriana: {added} new products")
        return added
    
    def scrape_lacomer(self):
        """Scrape La Comer"""
        
        initial_count = len(self.products)
        store_count = 0
        
        # La Comer search terms (expanded categories)
        search_terms = [
            'despensa', 'bebidas', 'lacteos', 'limpieza', 'cuidado personal',
            'carnes', 'frutas', 'verduras', 'panaderia', 'botanas',
            'congelados', 'refrigerados', 'salchichoneria', 'quesos',
            'cereales', 'enlatados', 'pastas', 'arroz', 'aceites',
            'salsas', 'condimentos', 'dulces', 'chocolates', 'galletas',
            'cafe', 'te', 'jugos', 'refrescos', 'agua',
            'cervezas', 'licores', 'snacks', 'papas', 'semillas'
        ]
        
        succ_id = 287  # La Comer store ID
        
        for term in search_terms:
            for page in range(1, 100):  # Increased pages to get all products
                try:
                    # Use the search API endpoint
                    url = "https://lacomer.buscador.amarello.com.mx/searchArtPrior"
                    params = {
                        'col': 'lacomer_2',
                        'npagel': 40,  # Results per page
                        'p': page,
                        'patrocinados': 'false',
                        's': term,
                        'succId': succ_id,
                        'topsort': 'false'
                    }
                    
                    # Retry logic for network issues
                    response = None
                    for attempt in range(3):
                        try:
                            response = requests.get(url, params=params, headers=self.headers, timeout=15)
                            break
                        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                            if attempt < 2:
                                time.sleep(2)
                            else:
                                raise
                    
                    if not response:
                        break
                    
                    if response.status_code != 200:
                        break
                    
                    data = response.json()
                    products_data = data.get('res', [])
                    
                    if not products_data:
                        break
                    
                    for item in products_data:
                        sku = str(item.get('artCod', ''))
                        if not sku:
                            continue
                        
                        # Extract all barcode fields
                        art_ean = str(item.get('artEan', '')) if item.get('artEan') else ''
                        ean13 = art_ean if art_ean else self.generate_ean13(sku)
                        upc = self.generate_upc(sku)
                        
                        # Use EAN13 as the primary identifier
                        if not self.is_unique_product(ean13):
                            continue
                        
                        price = item.get('artPrven', 0)
                        list_price = item.get('artPrlin', price)
                        
                        # Build image URL
                        image_url = ''
                        if item.get('artImg') == 1:
                            image_url = f"https://www.lacomer.com.mx/superc/img_art/{art_ean}_1.jpg"
                        
                        local_image = self.download_image(image_url, ean13)
                        
                        product = {
                            'sku': sku,
                            'ean13': ean13,
                            'upc': upc,
                            'ean': art_ean,
                            'art_cod': sku,
                            'name': item.get('artDes', '').strip(),
                            'brand': item.get('marDes', 'Sin Marca').strip(),
                            'category': item.get('agruDesPadre', term.title()),
                            'subcategory': item.get('agruDes', ''),
                            'price': float(price) if price else 0.0,
                            'list_price': float(list_price) if list_price else float(price) if price else 0.0,
                            'currency': 'MXN',
                            'available': float(item.get('inveCant', 0)) > 0,
                            'stock': int(float(item.get('inveCant', 0))),
                            'image_url': '',
                            'local_image': local_image,
                            'product_url': f"https://www.lacomer.com.mx/lacomer/#!/item/{sku}",
                            'store': 'La Comer',
                            'description': item.get('artDesCom', ''),
                            'unit_multiplier': float(item.get('artUco', 1)),
                            'measurement_unit': item.get('artTun', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.save_product(product)
                        store_count += 1
                        
                        if store_count % 100 == 0:
                            print(f"\rLa Comer: {store_count} products", end='', flush=True)
                    
                    time.sleep(random.uniform(0.3, 0.8))
                    
                except Exception as e:
                    continue
        
        added = len(self.products) - initial_count
        return added
    
    def scrape_bodega_aurrera(self):
        """Scrape Bodega Aurrera (Walmart Mexico) - Uses GraphQL API"""
        print("\n" + "="*60)
        print("SCRAPING BODEGA AURRERA")
        print("="*60)
        
        initial_count = len(self.products)
        
        # Bodega Aurrera uses GraphQL API at despensa.bodegaaurrera.com.mx
        # Categories to search
        search_terms = [
            'leche', 'pan', 'arroz', 'frijol', 'aceite', 'pollo', 'carne',
            'agua', 'refresco', 'jugo', 'yogurt', 'queso', 'jamon', 'huevo',
            'pasta', 'atun', 'galleta', 'cereal', 'cafe', 'azucar', 'sal',
            'jabon', 'shampoo', 'detergente', 'papel'
        ]
        
        print("  NOTE: Bodega Aurrera GraphQL API requires authentication/cookies")
        print("  Skipping for now - API endpoint needs proper headers/session")
        
        # GraphQL endpoint structure (for future implementation):
        # URL: https://despensa.bodegaaurrera.com.mx/orchestra/snb/graphql/Browse/{hash}/browse
        # Requires full variables object with tenant, page, limit, etc.
        # Currently returns 400 without proper authentication
        
        # Placeholder implementation for when API access is resolved
        for term in search_terms[:3]:  # Limit attempts
            print(f"  Searching: {term}")
            try:
                # GraphQL variables structure
                variables = {
                    "query": term,
                    "page": 1,
                    "prg": "desktop",
                    "limit": 40,
                    "ps": 40,
                    "sort": "best_match",
                    "tenant": "MX_BODEGA_OD_GLASS",
                    "pageType": "SearchPage"
                }
                
                url = "https://despensa.bodegaaurrera.com.mx/orchestra/snb/graphql/Browse/3b61d1ecc030bed143d8733c32b69c171f903bd9d9f0c2f6487656e3fd5a7187/browse"
                
                response = requests.get(
                    url,
                    params={'variables': json.dumps(variables)},
                    headers={**self.headers, 'Referer': 'https://despensa.bodegaaurrera.com.mx/'},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Parse GraphQL response structure here when working
                    print(f"    Got response: {response.status_code}")
                else:
                    print(f"    API returned {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"    Error: {str(e)[:50]}")
                break
        
        added = len(self.products) - initial_count
        print(f"[OK] Bodega Aurrera: {added} new products")
        return added
    
    def scrape_papelerias_tony(self):
        """Scrape Papelerias Tony - Office supplies and stationery"""
        initial_count = len(self.products)
        store_count = 0
        
        # Tony categories - expanded stationery, office, art supplies, etc.
        search_terms = [
            'escolar', 'oficina', 'arte', 'plumas', 'lapices', 'cuadernos',
            'mochilas', 'papel', 'carpetas', 'colores', 'marcadores', 'pegamento',
            'tijeras', 'calculadora', 'archivero', 'engrapadora', 'clips',
            'borradores', 'sacapuntas', 'reglas', 'compas', 'pintura', 'pinceles',
            'crayones', 'acuarelas', 'temperas', 'plumon', 'resaltador', 'corrector',
            'goma', 'cinta', 'adhesiva', 'hojas', 'cartulina', 'foami',
            'diamantina', 'silicones', 'pistola', 'plastilina', 'porcelana',
            'lienzo', 'caballete', 'estuche', 'lonchera', 'lapicera',
            'agenda', 'libreta', 'block', 'folder', 'mica', 'broche',
            'perforadora', 'sello', 'almohadilla', 'etiqueta', 'separadores'
        ]
        
        for term in search_terms:
            # VTEX search API with pagination
            for page in range(0, 50):  # Increased pages to get more products
                try:
                    _from = page * 50
                    _to = _from + 49
                    
                    url = "https://www.tony.com.mx/api/catalog_system/pub/products/search"
                    params = {
                        'ft': term,
                        '_from': _from,
                        '_to': _to
                    }
                    
                    # Retry logic for network issues
                    response = None
                    for attempt in range(3):
                        try:
                            response = requests.get(url, params=params, headers=self.headers, timeout=15)
                            break
                        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                            if attempt < 2:
                                time.sleep(2)
                            else:
                                raise
                    
                    if not response or response.status_code not in [200, 206]:
                        break
                    
                    data = response.json()
                    
                    if not data:
                        break
                    
                    page_products = 0
                    for item in data:
                        product_id = str(item.get('productId', ''))
                        if not product_id:
                            continue
                        
                        # Get all barcode fields from items
                        items = item.get('items', [])
                        ean13 = ''
                        upc = ''
                        item_ean = ''
                        if items:
                            item_ean = str(items[0].get('ean', '')) if items[0].get('ean') else ''
                            ean13 = item_ean if item_ean else self.generate_ean13(product_id)
                            upc = self.generate_upc(product_id)
                        else:
                            ean13 = self.generate_ean13(product_id)
                            upc = self.generate_upc(product_id)
                        
                        # Use EAN13 as the primary identifier
                        if not self.is_unique_product(ean13):
                            continue
                        
                        # Get reference codes
                        product_reference = str(item.get('productReference', '')) if item.get('productReference') else ''
                        product_reference_code = str(item.get('productReferenceCode', '')) if item.get('productReferenceCode') else ''
                        
                        # Price info
                        price = 0
                        list_price = 0
                        available = False
                        stock = 0
                        if items:
                            sellers = items[0].get('sellers', [])
                            if sellers:
                                commercial_offer = sellers[0].get('commertialOffer', {})
                                price = commercial_offer.get('Price', 0)
                                list_price = commercial_offer.get('ListPrice', price)
                                available = commercial_offer.get('IsAvailable', False)
                                stock = commercial_offer.get('AvailableQuantity', 0)
                        
                        # Image URL
                        image_url = ''
                        if items:
                            images = items[0].get('images', [])
                            if images:
                                image_url = images[0].get('imageUrl', '')
                        
                        local_image = self.download_image(image_url, ean13)
                        
                        # Get category from item
                        categories = item.get('categories', [])
                        category = categories[0].split('/')[1] if categories else term.title()
                        
                        product = {
                            'sku': product_id,
                            'ean': ean13 or item_ean,
                            'upc': upc,
                            'item_ean': item_ean,
                            'product_reference': product_reference,
                            'product_reference_code': product_reference_code,
                            'name': item.get('productName', '').strip(),
                            'brand': item.get('brand', 'Sin Marca') or 'Sin Marca',
                            'category': category,
                            'price': float(price) / 100 if price else 0.0,  # Tony prices are in centavos
                            'list_price': float(list_price) / 100 if list_price else float(price) / 100 if price else 0.0,
                            'currency': 'MXN',
                            'available': available,
                            'stock': int(stock),
                            'image_url': '',
                            'local_image': local_image,
                            'product_url': f"https://www.tony.com.mx{item.get('link', '')}",
                            'store': 'Papelerias Tony',
                            'description': item.get('description', ''),
                            'scraped_at': datetime.now().isoformat()
                        }
                        
                        self.save_product(product)
                        page_products += 1
                        store_count += 1
                        
                        if store_count % 100 == 0:
                            print(f"\rPapelerias Tony: {store_count} products", end='', flush=True)
                    
                    if page_products == 0:
                        break
                    
                    time.sleep(random.uniform(0.3, 0.8))
                    
                except Exception as e:
                    continue
        
        added = len(self.products) - initial_count
        return added
    
    def run(self):
        """Run all scrapers"""
        start_time = time.time()
        
        # Run all working scrapers (updates existing products)
        print("\nStarting Chedraui...")
        self.scrape_chedraui()          # ~2,548 products
        print("\nStarting La Comer...")
        self.scrape_lacomer()            # ~6,549 products
        print("\nStarting Papelerias Tony...")
        self.scrape_papelerias_tony()    # ~792 products
        # self.scrape_bodega_aurrera()   # GraphQL API requires auth/cookies
        # self.scrape_soriana()          # Skip for now, needs fixing
        
        elapsed = time.time() - start_time
        
        # Save to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"all_stores_products_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        
        return self.products

if __name__ == "__main__":
    # Configuration
    # Read MongoDB URI from environment if present (fallback to None)
    mongodb_uri = os.environ.get('MONGODB_URI') or None
    
    # Check SAVE_IMAGES environment variable (defaults to True)
    # Set SAVE_IMAGES=false or SAVE_IMAGES=0 to disable image downloading
    save_images_env = os.environ.get('SAVE_IMAGES', 'true').lower()
    save_images = save_images_env not in ['false', '0', 'no', 'off']
    
    debug_raw = False  # Print raw source data from first product per store
    
    print(f"[Config] MongoDB URI: {'configured' if mongodb_uri else 'not set'}")
    print(f"[Config] Save images: {save_images}")
    
    scraper = MultiStoreScraper(mongodb_uri=mongodb_uri, save_images=save_images, debug_raw=debug_raw)
    products = scraper.run()
    
    print("\n\nDone.")
