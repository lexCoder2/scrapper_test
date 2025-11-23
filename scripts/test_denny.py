import requests
from bs4 import BeautifulSoup
import json

print("Testing dulceriasdenny.com structure...\n")

# Test main productos page
url = "https://dulceriasdenny.com/productos"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for product cards/links
        product_links = soup.find_all('a', href=lambda x: x and '/producto/' in x)
        print(f"\nFound {len(product_links)} product links")
        
        if product_links:
            # Get first product URL
            first_product_url = product_links[0].get('href')
            if not first_product_url.startswith('http'):
                first_product_url = 'https://dulceriasdenny.com' + first_product_url
            
            print(f"First product URL: {first_product_url}")
            
            # Fetch first product page
            print("\nFetching product page...")
            pr = requests.get(first_product_url, headers=headers, timeout=10)
            
            if pr.status_code == 200:
                print(f"Product page status: {pr.status_code}")
                
                # Look for JSON data in script tags
                psoup = BeautifulSoup(pr.text, 'html.parser')
                scripts = psoup.find_all('script', type='application/ld+json')
                
                if scripts:
                    print(f"\nFound {len(scripts)} JSON-LD scripts")
                    for i, script in enumerate(scripts[:2]):
                        try:
                            data = json.loads(script.string)
                            print(f"\nScript {i+1}:")
                            print(json.dumps(data, indent=2))
                        except:
                            pass
                
                # Look for product data
                title = psoup.find('h1', class_=lambda x: x and ('product' in str(x).lower() or 'title' in str(x).lower()))
                price = psoup.find(lambda tag: tag.name in ['span', 'div', 'p'] and 'price' in str(tag.get('class', [])).lower())
                
                if title:
                    print(f"\nProduct title: {title.get_text(strip=True)}")
                if price:
                    print(f"Product price: {price.get_text(strip=True)}")
        
        # Look for any API endpoints in page source
        if 'api' in r.text.lower():
            print("\n'api' found in page source - may have API endpoints")
            
except Exception as e:
    print(f"Error: {e}")
