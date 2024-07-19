import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import json
from tqdm import tqdm  # Import tqdm for the progress bar

def get_all_categories(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    # Using XPath to extract href attributes
    all_category = tree.xpath('//*[@id="main"]/article/section[1]/ul/li/ul/li/a/@href')
    return all_category

def get_scripted_tags(script_tags):
    data = None
    for script in script_tags:
        try:
            script_data = json.loads(script.string)
            if script_data.get('@type') == 'ItemList':
                data = script_data
                break
        except (json.JSONDecodeError, KeyError):
            continue
    return data

def get_product_details(data):
    urls = []
    for item in data.get('itemListElement', []):
        if not item.get('url') in urls:
            urls.append(item.get('url'))    
    return urls

def clean_elements(elements):
    if elements:
        return ' '.join(element.strip() for element in elements if element.strip())
    return ''

def clean_text(text):
    return re.sub(r'[\xa0\u200b]', ' ', text).strip()

def extract_price(text):
    cleaned_text = clean_text(text)  
    match = re.search(r'£\d+\.\d+', cleaned_text)
    return match.group(0)[1] if match else ''

def clean_price_per_kg(text):
    kg_price =  clean_text(text)
    return kg_price[1:]

def extract_product_info(product_url):
    response = requests.get(product_url)
    data = html.fromstring(response.content)
    
    title = clean_elements(data.xpath('.//h1/text()'))
    url = response.url
    image = data.xpath('.//img[@class="productImages__image"]/@src')
    description = clean_elements(data.xpath('.//div[@class="productDescription"]/div/text()'))
    consume_advise = clean_elements(data.xpath('.//p[@class="consumeAdvices"]/text()'))
    product_weight = clean_elements(data.xpath('.//p[@class="productCard__weight"]/text()'))
    ingredients = clean_elements(data.xpath('.//h3[contains(text(),"Ingredients")]/following::p[1]/text()'))
    nutrition_value = clean_elements(data.xpath('.//h3[contains(text(),"Nutritional values")]/following::p[1]/text()'))
    allergens = clean_elements(data.xpath('.//h3[contains(text(),"Allergens")]/following::p[1]/text()'))
    vegan = clean_elements(data.xpath('.//h3[contains(text(),"Vegan")]/following::p[1]/text()'))
    price_per_kg_text = clean_elements(data.xpath('.//h3[contains(text(),"Price per kilo")]/following::p[1]/text()'))
    price_per_kg = clean_price_per_kg(price_per_kg_text)
    price_text = clean_elements(data.xpath('.//button[@data-button-action="add-to-cart"]/text()'))
    price = extract_price(price_text)
    manufacturing = clean_elements(data.xpath('.//div[@class="productManufacturing__text wysiwyg-content"]/p/text()'))
    
    return {
        'title': title,
        'URL': url,
        'image': image,
        'price': price,
        'description': description,
        'consume_advise': consume_advise,
        'product_weight': product_weight,
        'ingredients': ingredients,
        'nutrition_value': nutrition_value,
        'allergens': allergens,
        'vegan': vegan,
        'price_per_kg': price_per_kg,
        'manufacturing': manufacturing
    }

# Main URL
sitemap_url = "https://www.lechocolat-alainducasse.com/uk/sitemap"

# Get all categories from sitemap
categories = get_all_categories(sitemap_url)
all_products = []

# Loop through each category to extract product details
for category in tqdm(categories, desc="Processing Categories", unit="category"):
    response = requests.get(category)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script', {'type': 'application/ld+json'})
    
    data = get_scripted_tags(script_tags)
    if data:
        product_urls = get_product_details(data)
        for product_url in tqdm(product_urls, desc="Processing Products", unit="product", leave=False):
            product_info = extract_product_info(product_url)
            all_products.append(product_info)

# Save all product information to output.json
with open('output/lechocolate_output.json', 'w') as json_file:
    json.dump(all_products, json_file, indent=4)

print("Data has been saved to lechocolate_output.json")

