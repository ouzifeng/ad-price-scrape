import requests
from bs4 import BeautifulSoup
import csv
import os
import time
from concurrent.futures import ThreadPoolExecutor
import requests_cache

# Enable caching
requests_cache.install_cache('prices_cache')

MAX_URLS = 50000
NUM_WORKER_THREADS = 10

# Get path to folder where script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Open the generated CSV file
with open(os.path.join(folder_path, 'prices.csv'), mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Read URLs from CSV file
urls = []
with open(os.path.join(folder_path, 'urls.csv'), mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        urls.append(row[0])

        if len(urls) >= MAX_URLS:
            break

 # Check if URLs have already been scraped and load them
scraped_urls_file = os.path.join(folder_path, 'scraped_urls.txt')
if os.path.exists(scraped_urls_file):
    with open(scraped_urls_file, mode='r') as file:
        scraped_urls = set(file.read().splitlines())
else:
    scraped_urls = set()

# Create CSV file and write headers
with open(os.path.join(folder_path, 'prices.csv'), mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        ['Product Name', 'Variation Data', 'MPN', 'Price', 'Stock'])

    # Create a set to store URLs that have already been scraped
    scraped_urls = set()

    # Create a thread pool with worker threads
    with ThreadPoolExecutor(max_workers=NUM_WORKER_THREADS) as executor:
        # Use the requests_cache module to cache the responses
        requests_cache.install_cache('prices_cache')

        # Keep track of start time
        start_time = time.time()

        # Loop through the URLs and scrape data
        for i, url in enumerate(urls):
            # Skip URLs that have already been scraped
            if url in scraped_urls:
                continue

            # Send request and get response
            future = executor.submit(requests.get, url)

            try:
                response = future.result()

                # Add the URL to the set of scraped URLs
                scraped_urls.add(url)

                # Parse HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, 'lxml')

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

                # Find stock availability
                stock = ""
                stock_element = soup.find('div', {'class': 'stock'})
                if stock_element:
                    if 'unavailable' in stock_element.get('class', []):
                        stock = 'Out of stock'
                    elif 'available' in stock_element.get('class', []):
                        stock = 'In stock'

                # Clean and store MPNs and prices in a dictionary
                mpn_price_dict = {}
                for price in prices:
                    price_text = price.text.strip()
                    if 'From:' not in price_text:
                        # Remove non-ASCII characters from the price string
                        price_text = ''.join(
                            filter(lambda x: ord(x) < 128, price_text))
                        for mpn in mpns:
                            mpn_text = mpn.text.strip()
                            if mpn_text:
                                mpn_price_dict[mpn_text] = price_text

                # Write data rows
                for mpn, price in mpn_price_dict.items():
                    writer.writerow([product_name, variation_data,
                                     mpn, price, stock])

                # Print progress every 10 URLs
                if i % 10 == 0:
                    print(f"Scraped {i}/{len(urls)} URLs...")

            except Exception as e:
                print(f"Error scraping URL: {url}")
                print(e)
