# Product Scraper
This Python script extracts product data from a specified WooCommerce website and exports the data to a CSV file. It utilizes Selenium for web scraping and requests_html for parsing HTML content.

## Table of Contents
**Installation**
**Usage**
**Generate SKU**
**Run the Script**
**Customization**
**Notes**

## Installation
Before running the script, you need to set up your environment and install the necessary dependencies.

### Prerequisites
**Python 3.x**
**ChromeDriver (Make sure it's compatible with your Chrome version)**
**Google Chrome**
**Install Dependencies**
```
pip install requests-html selenium
```
### Setup ChromeDriver
Download the appropriate ChromeDriver for your Chrome version.
Extract the ChromeDriver and place it in a directory of your choice.
Update the chromedriver_path variable in the script with the path to the ChromeDriver executable.
## Usage
### Generate SKU
The script uses a function to generate a random SKU (Stock Keeping Unit) for each product. The SKU is a 10-digit random number.

### Run the Script
1. Modify the url variable in the script to the specific WooCommerce page URL from which you want to scrape products.

2. Run the script:

```
python product_scraper.py
```
The script will automatically scroll through the specified webpage to load all products and then extract product data, including:

1. Product Name
2. SKU
3. Price
4. Sale Price (if available)
5. Image URL
6. Short Description
7. Additional Attributes (e.g., price per kg, kosher, validity, unit weight)
The extracted data will be saved to a CSV file named promotions.csv in the same directory as the script.

## Customization
You may need to adjust the CSS selectors in the get_productdata function to match the HTML structure of the target WooCommerce site. Here are some of the customizable elements:

**Title Element**: 'h1.product_title.entry-title'
**Price Container**: 'div.elementor-element-ef626ed'
**Image Element**: 'div.woocommerce-product-gallery__image img'
**Short Description**: 'div.woocommerce-product-details__short-description'
**Additional Attributes**: 'div.elementor-element-e68a7ce', 'div.elementor-element-27b065b', etc.
## Notes
The script is designed to work with WooCommerce websites that follow a specific structure. If your target website has a different structure, you may need to adjust the CSS selectors accordingly.
Adjust the time.sleep() durations as needed to ensure all products load correctly during scrolling.


## Created By
Qusai Safa 
email : qusi.bassam@gmail.com