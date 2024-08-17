from requests_html import HTMLSession
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import random

def generate_sku():
    sku = ''.join(random.choices('0123456789', k=10))
    return sku

# Path to chromedriver executable (change this to you driver path)
# you can download chrome driver from this link https://developer.chrome.com/docs/chromedriver/downloads
chromedriver_path = '/Users/qusaisafa/chromedriver/chromedriver'

# URL of woocomerce site to get a copy of its product (provide spacific page)
url = 'Add url here'

# Initialize Selenium WebDriver
chrome_options = ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=ChromeService(executable_path=chromedriver_path), options=chrome_options)
driver.get(url)

# Scroll down to the bottom of the page to load all products
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)  # Adjust sleep time as needed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract links from the loaded page
links = []
elements = driver.find_elements(By.CSS_SELECTOR, 'a.elementor-element-4a3a34e')
print(len(elements))

for element in elements:
    href = element.get_attribute('href')
    if href:
        if href not in links:
            links.append(href)
print(len(links))

# Function to retrieve product data given a link
def get_productdata(link):
    session = HTMLSession()
    if link:
        r = session.get(link)
        # products html tag (css class of the products) this is the default one
        title_element = r.html.find('h1.product_title.entry-title', first=True)
        title = title_element.text.strip() if title_element else ""
        
        # change this to your price container html tag
        price_container = r.html.find('div.elementor-element-ef626ed ', first=True)
        # product might contain 2 tags(sale price and regular price)
        if price_container:
            price_elements = price_container.find('span.woocommerce-Price-amount.amount bdi')
            price = price_elements[0].text.strip() if price_elements else ""
            second_price = price_elements[1].text.strip() if len(price_elements) > 1 else ""
        else:
            price = ""
            second_price = ""

        image_element = r.html.find('div.woocommerce-product-gallery__image img', first=True)
        image_url = image_element.attrs['src'] if image_element else ""

        price_per_kg_element = r.html.find('div.elementor-element-e68a7ce .elementor-widget-container', first=True)
        price_per_kg = price_per_kg_element.text.split(":")[-1].strip() if price_per_kg_element else ""

        kosher_element = r.html.find('div.elementor-element-27b065b .elementor-widget-container', first=True)
        kosher = kosher_element.text.split(":")[-1].strip() if kosher_element else ""

        validity_element = r.html.find('div.elementor-element-f1d72a6 .elementor-widget-container', first=True)
        validity = validity_element.text.split(":")[-1].strip() if validity_element else ""

        unit_weight_element = r.html.find('div.elementor-element-76c0ef4 .elementor-widget-container', first=True)
        unit_weight = unit_weight_element.text.split(":")[-1].strip() if unit_weight_element else ""

        short_desc = r.html.find('div.woocommerce-product-details__short-description', first=True)
        short_desc = short_desc.text.split(":")[-1].strip() if short_desc else ""

        product = {
            'Name': title,
            'SKU': generate_sku(),
            'Type': 'simple',
            'Published': 1,
            'is featured?': 0,
            'Visibility in catalog': 1,
            'In stock?': 1,
            'Categories':"set you category here",
            'Regular price': price,
            'Sale price': second_price,
            'Images': image_url,
            'Short description': short_desc,
            'Visibility in catalog': 'visible',
            'Attribute 1 name': 'price_per_kg', # this optional
            'Attribute 1 value(s)': price_per_kg,
            'Attribute 1 visible': 1 if price_per_kg is not None and price_per_kg != '' else 0,
            'Attribute 1 global': 1 if price_per_kg is not None and price_per_kg != '' else 0,
            'Attribute 2 name': 'kosher', # this optional
            'Attribute 2 value(s)': kosher,
            'Attribute 2 visible': 1 if kosher is not None and kosher != '' else 0,
            'Attribute 2 global': 1 if kosher is not None and kosher != '' else 0,
            'Attribute 3 name': 'validity', # this optional
            'Attribute 3 value(s)': validity,
            'Attribute 3 visible': 1 if validity is not None and validity != '' else 0,
            'Attribute 3 global': 1 if validity is not None and validity != '' else 0,
            'Attribute 4 name': 'unit_weight', # this optional
            'Attribute 4 value(s)': unit_weight,
            'Attribute 4 visible': 1 if unit_weight is not None and unit_weight != '' else 0,
            'Attribute 4 global': 1 if unit_weight is not None and unit_weight != '' else 0,
        }
    else:
        product = {}  # Handle case where link is None

    session.close()
    return product

# Retrieve product data for each link
results = []
for link in links:
    results.append(get_productdata(link))
    time.sleep(1)  # Adjust sleep time as needed

# Write results to CSV
with open('promotions.csv', 'w', encoding='utf8', newline='') as f:
    fc = csv.DictWriter(f, fieldnames=results[0].keys())
    fc.writeheader()
    fc.writerows(results)

print("Scraping completed and results saved to fish.csv")

# Close the browser
driver.quit()
