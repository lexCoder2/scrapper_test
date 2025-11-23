import requests
import json
from urllib.parse import unquote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'es-MX,es;q=0.9',
    'Referer': 'https://despensa.bodegaaurrera.com.mx/'
}

print("Testing Bodega Aurrera GraphQL API...")
print("="*60)

# Full variables structure from the URL
variables = {
    "id": "",
    "dealsId": "",
    "query": "",
    "nudgeContext": "",
    "page": 1,
    "prg": "desktop",
    "catId": "06_0601",
    "facet": "",
    "sort": "best_match",
    "rawFacet": "",
    "seoPath": "",
    "ps": 10,
    "limit": 10,
    "ptss": "",
    "trsp": "",
    "beShelfId": "",
    "recall_set": "",
    "module_search": "",
    "min_price": "",
    "max_price": "",
    "storeSlotBooked": "",
    "additionalQueryParams": {
        "hidden_facet": None,
        "translation": None,
        "isMoreOptionsTileEnabled": True,
        "rootDimension": "",
        "altQuery": "",
        "selectedFilter": "",
        "neuralSearchSeeAll": False,
        "isLMPBrowsePage": False
    },
    "searchArgs": {
        "query": "",
        "cat_id": "06_0601",
        "prg": "desktop",
        "facet": ""
    },
    "ffAwareSearchOptOut": False,
    "enableCopyBlock": True,
    "enableVariantCount": False,
    "enablePortableFacets": True,
    "tenant": "MX_BODEGA_OD_GLASS",
    "pageType": "BrowsePage",
    "enableFacetCount": True,
    "marketSpecificParams": "{\"banner\":\"od\",\"pageType\":\"browse\",\"locale\":\"es_MX\"}",
    "fetchMarquee": True,
    "fetchSkyline": True
}

url = "https://despensa.bodegaaurrera.com.mx/orchestra/snb/graphql/Browse/3b61d1ecc030bed143d8733c32b69c171f903bd9d9f0c2f6487656e3fd5a7187/browse"

try:
    response = requests.get(url, params={'variables': json.dumps(variables)}, headers=headers, timeout=15)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type')}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse keys: {list(data.keys())}")
        
        # Navigate to products
        if 'data' in data:
            print(f"\nData keys: {list(data['data'].keys())}")
            if 'search' in data['data']:
                search = data['data']['search']
                print(f"\nSearch keys: {list(search.keys())}")
                
                if 'searchResult' in search:
                    result = search['searchResult']
                    print(f"\nSearch Result keys: {list(result.keys())}")
                    
                    if 'itemStacks' in result:
                        items = result['itemStacks']
                        print(f"\nNumber of items: {len(items)}")
                        
                        if items:
                            print(f"\nFirst item structure:")
                            print(json.dumps(items[0], indent=2, ensure_ascii=False)[:2000])
    else:
        print(f"Error: {response.text[:500]}")
        
except Exception as e:
    print(f"Exception: {type(e).__name__}: {e}")
