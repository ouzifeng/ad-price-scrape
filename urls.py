import requests
import xml.etree.ElementTree as ET
import csv

# URLs of sitemaps
sitemaps = [
    'https://www.anglingdirect.co.uk/pub/sitemap/sitemap-5-1.xml',
    'https://www.anglingdirect.co.uk/pub/sitemap/sitemap-5-2.xml',
    'https://www.anglingdirect.co.uk/pub/sitemap/sitemap-5-3.xml',
    'https://www.anglingdirect.co.uk/pub/sitemap/sitemap-5-4.xml',
    'https://www.anglingdirect.co.uk/pub/sitemap/sitemap-5-5.xml'
]

# List to hold URLs
url_list = []

# Counter for number of URLs processed
count = 0

# Loop through sitemaps and extract URLs
for sitemap_url in sitemaps:
    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)
    for child in root:
        if count >= 20159:
            url = child[0].text
            url_list.append(url)
        count += 1

# Write URLs to CSV file
with open('urls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['URL'])
    for url in url_list:
        writer.writerow([url])
