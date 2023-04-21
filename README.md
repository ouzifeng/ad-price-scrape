# ad-price-scrape
These scripts help pull prices from Angling Direct www.anglingdirect.co.uk

It does a few cool things:

1. Scrapes variation and variable products
2. Captures prices
3. Captures variation information and SKU - i.e. if it is the Kamakura hook range it will create Kamakura size 8, 10 etc
4. Captures stock - either in stock or out of stock. Typical AD dont always show the amount of stock for each product so this is the safest way
5. It builds a DB of urls from their sitemap before scraping. This makes it much more stable than scraping directly
6. Uses multi threadcore to scrape more than 1 url at once
7. Creates a cache which speeds up subsequent scrapes massively
8. Creates a log.txt as it scrapes so if it crashes it can pickup where it leaves off, although the log is massive (6gb)


This is a 2 part scrape, the reason why you cannot built the url directory and run the scrape in the one script is that it often crashes. Building a CSV of URLs first makes it mich more stable

Step 1:

Run the urls.py This will generate a CSV with all ADs urls, it takes it from their sitemaps. The first 25k"ish" URLs are not product related, i.e anglingdirect.co.uk/brand/x etc, so the script removes none product related URLs the best it can

Step 2:
Once you have the CSV in the same folder as the prices.py run the prices script. This will generate a "prices.csv" file

Couple of things to point out:
1. It adds a ^ in front of all prices, i.e. ^£9.99. I cannot get the script to remove this despite there being a function in there to do so. It's not such a big issue that I felt I needed to invest more time into as you can remove them from the CSV
2. The terminal gives you a lot of info i.e. number of urls in total, how far in it is etc
3. As it goes it builds up an html cache. This cache is large (6gb), but means next time you run it it is going to be 4-5x faster
4. It also generates a log so that if it falls over/your PC turns off etc, you can run it again and it will pickup where it is left off

I have added the sample URL and Prices CS for you to have a look, but these will be well out of date.

If this runs with errors it is probably due to AD changing their schema and will be a quick fix, reach out if you need help. Inital scrape time for me was about 6-8 hours
