import requests
from bs4 import BeautifulSoup
import csv
import os

MAX_URLS = 50000

# Get path to desktop
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Read URLs from CSV file
urls = []
with open(os.path.join(desktop_path, 'urls.csv'), mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        urls.append(row[0])

        if len(urls) >= MAX_URLS:
            break

# Create CSV file and write headers
with open(os.path.join(desktop_path, 'prices.csv'), mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Variation Data', 'MPN', 'Price'])

    # Loop through the URLs and scrape data
    for i, url in enumerate(urls):
        # Send request and get response
        response = requests.get(url)

        try:
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find product name, variation data, MPNs, and prices
            product_name = soup.find('h1', {'class': 'page-title'})
            if product_name:
                product_name = product_name.text.strip()
            else:
                product_name = ""
            variation_data = soup.find(
                'strong', {'class': 'product-item-name'})
            if variation_data:
                variation_data = variation_data.text.strip()
            else:
                variation_data = ""
            mpns = soup.find_all('span', {'class': 'product-item-model'})
            if not mpns:
                mpns = soup.find_all('span', {'itemprop': 'mpn'})
            prices = soup.find_all('span', {'class': 'price'})

            # Clean and store MPNs and prices in lists
            clean_mpns = [mpn.text.strip() for mpn in mpns]
            clean_prices = []
            for price in prices:
                price_text = price.text.strip()
                if 'From:' not in price_text:
                    # Remove the "Â" character from the price string
                    price_text = price_text.replace('Â', '')
                    clean_prices.append(price_text)

            # Write data rows
            for j in range(len(clean_mpns)):
                writer.writerow([product_name, variation_data,
                                 clean_mpns[j], clean_prices[j]])

            # Print progress every 10 URLs
            if i % 10 == 0:
                print(f"Scraped {i}/{len(urls)} URLs...")

        except Exception as e:
            print(f"Error scraping URL: {url}")
            print(e)
