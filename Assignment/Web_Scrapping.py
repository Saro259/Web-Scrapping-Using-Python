import requests
from bs4 import BeautifulSoup
import csv

# set the headers and user agent to prevent Amazon from blocking the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

# set the number of pages to scrape
num_pages = 20

# open a CSV file to write the scraped data
with open('amazon_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # write the header row of the CSV file
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                     'Description', 'ASIN', 'Product Description', 'Manufacturer'])

    # loop through the pages and scrape the required information
    for page in range(1, num_pages + 1):
        print('Scraping page', page)
        # send a GET request to the URL with the page number
        response = requests.get(url.format(page), headers=headers)
        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all the product listings on the page
        products = soup.find_all('div', {'class': 's-result-item'})

        # loop through the product listings and scrape the required information
        for product in products:
            # extract the product URL, product name, product price, rating, and number of reviews
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            product_name = product.find('span', {'class': 'a-size-medium'}).string.strip()
            product_price = product.find('span', {'class': 'a-price-whole'}).string.strip()
            rating = product.find('i', {'class': 'a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom'}).string.strip()
            num_reviews = product.find('span', {'class': 'a-size-base'}).string.strip()

            # send a GET request to the product URL
            response = requests.get(product_url, headers=headers)
            # parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # extract the product description, ASIN, and manufacturer
            try:
                description = soup.find('div', {'id': 'productDescription'}).text.strip()
            except AttributeError:
                description = ''
            asin = soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
            try:
                product_description = soup.find('div', {'id': 'productDescription'}).find('p').text.strip()
            except AttributeError:
                product_description = ''
            manufacturer = soup.find('th', text='Manufacturer').find_next_sibling('td').text.strip()

            # write the scraped data to the CSV file
            writer.writerow([product_url, product_name, product_price, rating, num_reviews, description, asin, product_description, manufacturer])