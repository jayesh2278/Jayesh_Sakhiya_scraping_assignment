import re
import json
import os
import requests

class Validation:
    def __init__(self, data):
        self.data = data
        self.errors = []

    def validate(self):
        self.validate_mandatory_fields()
        self.validate_url_format()
        self.validate_image_url_format()
        self.validate_unique_ids()
        self.is_url_accessible()
        self.validate_price()
        return self.errors

    def validate_mandatory_fields(self):
        mandatory_fields = ['title','URL', 'image']
        for item in self.data:
            for field in mandatory_fields:
                if field not in item or not item[field]:
                    self.errors.append(f"Missing mandatory field: {field} in item {item}")

    def validate_url_format(self):
        url_pattern = re.compile(
            r'^(https?:\/\/)?'  # http or https
        )
        for item in self.data:
            if not re.match(url_pattern, item['URL']):
                self.errors.append(f"Invalid URL format in item {item}")
            



    def validate_image_url_format(self):
        image_pattern = re.compile(r'^(https?:\/\/)', re.IGNORECASE)  # Ensure it starts with http:// or https://

        for item in self.data:
            images = item.get('image')

            if isinstance(images, str):
                # Check if the single string image URL is valid
                if not re.match(image_pattern, images):
                    self.errors.append(f"Invalid image URL format in item {item}")
            elif isinstance(images, list):
                # Check each URL in the list
                for img in images:
                    if not isinstance(img, str) or not re.match(image_pattern, img):
                        self.errors.append(f"Invalid image URL format in item {item}")
            else:
                self.errors.append(f"Image field has an invalid type in item {item}")


    def is_url_accessible(self):
        for item in self.data:
            url = item.get('URL')
        try:
            response = requests.head(url, timeout=5)  # Use HEAD request to check URL availability
            if response.status_code not in range(200, 300):
                self.errors.append(f"URL not working (status code {response.status_code}): {url} in item {item}")
        except requests.RequestException:
            self.errors.append(f"URL not working (exception): {url} in item {item}")


    def validate_unique_ids(self):
        seen_ids = set()
        for item in self.data:
            if item.get('id'):
                item_id = item.get('id') 
                if item_id in seen_ids:
                    self.errors.append(f"Duplicate identifier found: {item_id} in item {item}")
                else:
                    seen_ids.add(item_id)

    def validate_price(self):
        price_pattern = re.compile(r'^\d+(\.\d{2})?$')  # Matches numbers with optional two decimal places

        for item in self.data:
            # Directly check the 'price' field on the item
            price = item.get('price')
            
            # If 'price' key is not present, skip validation for this item
            if price is None:
                continue

            if not isinstance(price, (int, float, str)):
                self.errors.append(f"Invalid price type in item: {price} in item {item}")
                continue

            # Convert to string if it's a number
            if isinstance(price, (int, float)):
                price = str(price)

            # Check if the price format is valid
            if not re.match(price_pattern, price):
                self.errors.append(f"Invalid price format in item: {price} in item {item}")

            # Optionally, check if the price falls within a specific range
            try:
                price_value = float(price)
                if price_value < 0:  # Example range check
                    self.errors.append(f"Price is negative in item: {price} in item {item}")
            except ValueError:
                self.errors.append(f"Invalid price value in item: {price} in item {item}")


                


def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data
 
def find_json_files(folder_path):
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


# Example usage:
if __name__ == "__main__":
    folder_path = '/Users/jenishsakhiya/Desktop/Adeptmind' # Replace with your folder path
    json_files = find_json_files(folder_path)
    for json_file_path in json_files:
        data = load_json_data(json_file_path)
        validator = Validation(data)
        errors = validator.validate()
        print(errors)
