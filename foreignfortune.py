import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm  # Import tqdm for the progress bar

# URL of the sitemap
sitemap_url = "https://foreignfortune.com/sitemap_products_1.xml?from=943303098425&to=10150698057921"

# Fetch the sitemap content
response = requests.get(sitemap_url)
sitemap_content = response.content

# Parse the sitemap content
soup = BeautifulSoup(sitemap_content, 'xml')

# Regular expression to match the desired product URLs
product_url_pattern = re.compile(r'^https://foreignfortune\.com/products/')

# Find all product URLs that match the pattern
product_urls = [loc.text for loc in soup.find_all('loc') if product_url_pattern.match(loc.text)]

# Function to parse information from HTML page and convert to a Python dictionary
def extract_json(url):
    response = requests.get(url)
    page_content = response.content
    # Parse the product page content using html parser
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find the script tag with type application/ld+json
    script_tags = soup.find_all('script', {'type': 'application/ld+json'})

    # Ensure the correct script tag is selected
    data = None
    for script in script_tags:
        try:
            script_data = json.loads(script.string)
            if script_data.get('@type') == 'Product':
                data = script_data
                break
        except (json.JSONDecodeError, KeyError):
            continue

    if data:
        # Find the meta tag with property og:description
        meta_tag = soup.find('meta', {'property': 'og:description'})
        description = meta_tag['content'] if meta_tag else ''
        data['description'] = description

    return data

# Function to structure the data
def structure_data(data):
    structured_data = {
        'id': data['url'].replace("https://foreignfortune.com/products/", ''),
        'title': data['name'],
        'brand': data.get('brand').get('name'),
        'URL': data['url'],
        'image': data['image'][0] if isinstance(data['image'], list) else data['image'],
        'description': data.get('description', ''),
        'model': []
    }

    offers = data.get('offers', [])
    if not isinstance(offers, list):
        offers = [offers]

    for offer in offers:
        if 'itemOffered' in offer:
            item_offered = offer['itemOffered']
            model_info = {
                'name': item_offered.get('name', ''),
                'price': offer.get('price', ''),
                'priceCurrency': offer.get('priceCurrency', ''),
                'availability': offer.get('availability', ''),
                'url': offer.get('url', '')
            }
            structured_data['model'].append(model_info)

    return structured_data

final_product_list = []

# Process each product URL with a progress bar
for url in tqdm(product_urls, desc="Scraping Products", unit="product"):
    data = extract_json(url)
    if data:
        product_data = structure_data(data)
        final_product_list.append(product_data)

# Save the final product list to a JSON file
with open('output/foreignfortune_product.json', 'w') as json_file:
    json.dump(final_product_list, json_file, indent=4)

print("Data has been saved to foreignfortune_product.json")
