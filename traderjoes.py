import requests
import json
import os
from tqdm import tqdm  # Import tqdm for the progress bar

skus = []

def sku_data():
    url = "https://www.traderjoes.com/api/graphql"

    headers = {
        'accept': '*/*',
        'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,gu;q=0.7',
        'content-type': 'application/json',
        'cookie': 'YOUR_COOKIE_HERE',
        'dnt': '1',
        'origin': 'https://www.traderjoes.com',
        'priority': 'u=1, i',
        'referer': 'https://www.traderjoes.com/home/products/category/products-2',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    payload_template = {
        "query": "query SearchProducts($categoryId: String, $currentPage: Int, $pageSize: Int, $storeCode: String = \"TJ\", $availability: String = \"1\", $published: String = \"1\") {\n  products(\n    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}, category_id: {eq: $categoryId}}\n    currentPage: $currentPage\n    pageSize: $pageSize\n  ) {\n    items {\n      sku\n      item_title\n      category_hierarchy {\n        id\n        name\n        __typename\n      }\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      item_story_marketing\n      sales_size\n      sales_uom_description\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      fun_tags\n      item_characteristics\n      __typename\n    }\n    total_count\n    pageInfo: page_info {\n      currentPage: current_page\n      totalPages: total_pages\n      __typename\n    }\n    aggregations {\n      attribute_code\n      label\n      count\n      options {\n        label\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        "variables": {
            "storeCode": "TJ",
            "availability": "1",
            "published": "1",
            "categoryId": 2,
            "pageSize": 75,
            "currentPage": 1
        }
    }

    # Use tqdm for the page numbers
    for page_num in tqdm(range(1, 28), desc="Fetching SKUs", unit="page"):
        payload_template["variables"]["currentPage"] = page_num
        payload = json.dumps(payload_template)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            all_data = response.json()
            all_data = all_data['data']['products']['items']
            for data in all_data:
                if not data.get("sku") in skus:
                    skus.append(data.get("sku"))

def detail_product_data(skus):
    all_items_data = []
    
    # Use tqdm for the SKUs
    for sku in tqdm(skus, desc="Fetching Product Details", unit="sku"):
        url = "https://www.traderjoes.com/api/graphql"

        headers = {
            'accept': '*/*',
            'accept-language': 'en-IN,en-US;q=0.9,en;q=0.8,gu;q=0.7',
            'content-type': 'application/json',
            'cookie': 'YOUR_COOKIE_HERE',
            'dnt': '1',
            'origin': 'https://www.traderjoes.com',
            'priority': 'u=1, i',
            'referer': 'https://www.traderjoes.com/home/products/category/products-2',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        payload_template = {
            "query": "query SearchProduct($sku: String, $storeCode: String = \"TJ\", $published: String = \"1\") {\n  products(\n    filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "storeCode": "TJ",
                "published": "1",
                "sku": sku
            }
        }

        payload = json.dumps(payload_template)
        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if data['data']['products']['items']:
                product_item = data['data']['products']['items'][0]
                item_url = product_item.get("url_key")
                parts = item_url.split('-', 1)
                item_url = f"https://www.traderjoes.com/home/products/pdp/{parts[1]}-{parts[0]}"

                item_data = {
                    "id": product_item.get("sku"),
                    "title": product_item.get("item_title"),
                    "URL": item_url,
                    "image" : "https://www.traderjoes.com/home/"+ product_item.get("primary_image"),
                    "item_characteristics": product_item.get("item_characteristics"),
                    "description": product_item.get("item_story_qil"),
                    "sale_size": product_item.get("sales_size"),
                    "sales_uom_code": product_item.get("sales_uom_code"),
                    "sales_uom_description": product_item.get("sales_uom_description"),
                    "country_of_origin": product_item.get("country_of_origin"),
                    "price": product_item.get("retail_price"),
                }

                nutrition = product_item.get("nutrition")
                nutrition_list = []
                if nutrition:
                    nutrition = nutrition[0]
                    serving_size = nutrition.get("serving_size")
                    calories_per_serving = nutrition.get("calories_per_serving")

                    details = nutrition.get("details")
                    for detail in details:
                        n_data = {
                            "nutritional_item": detail.get("nutritional_item"),
                            "amount": detail.get("amount"),
                            "percent_dv": detail.get("percent_dv")
                        }
                        nutrition_list.append(n_data)
                else:
                    serving_size = ""
                    calories_per_serving = ""
                item_data["serving_size"] = serving_size
                item_data["calories_per_serving"] = calories_per_serving
                item_data["nutrition"] = nutrition_list

                ingredients = product_item.get("ingredients")
                ingredients_list = []
                if ingredients:
                    for ingredient in ingredients:
                        ingredients_list.append(ingredient.get('ingredient'))
                item_data["ingredients_list"] = ingredients_list

                all_items_data.append(item_data)
    
    return all_items_data

# Run the functions to fetch data
sku_data()
all_items = detail_product_data(skus)

# Save data to JSON file
output_file = 'output/traderjoes_output.json'
if os.path.exists(output_file):
    os.remove(output_file)

with open(output_file, 'w') as f:
    json.dump(all_items, f, indent=4)

print(f"Data saved to {output_file}")