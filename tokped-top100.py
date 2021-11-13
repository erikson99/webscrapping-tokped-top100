'''
=== Tokopedia Top 100 Products ===

Extracts top 100 products of category Mobile Phones/Handphones from Tokopedia and stores it in a csv file.

Input : producat category url
Output: csv file (tokopedia.csv)
        Include the following information:
        1. Name of Product
        2. Description
        3. Image Link
        4. Price
        5. Rating (out of 5 stars)
        6. Name of store or merchant

By: Erikson erixon@gmail.com
For: Brick Teknologi Indonesia

'''

# import required libraries
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# define user agent
header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}


# product scrapper utility
def product_scrapper():
    top100 = []

    for page in range(1,15):
        # product page for mobile phones category
        baseurl = f"https://www.tokopedia.com/p/handphone-tablet/handphone?page={page}"

        request = requests.get(baseurl, headers=header, timeout=5)
        html = BeautifulSoup(request.content, "html.parser")

        # get products container
        container = html.find('div', 'css-13l3l78 e1nlzfl10')

        # get products data
        products = container.findAll('div', 'css-bk6tzz e1nlzfl3')

        # get individual product data
        for product in products:
            product_name = product.find('span', 'css-1bjwylw').text
            product_desc = product_name
            product_image = product.find('div', 'css-1c0vu8l').img.get('src')
            product_price = product.find('span', 'css-o5uqvq').text
            store_name = product.findAll('span', 'css-1kr22w3')[1].text
            ratings = product.find('div', 'css-153qjw7')

            if ratings is not None:
                stars = [img['src'] for img in ratings.findAll('img')]
            else:
                stars = []

            num_stars = np.unique(stars, return_counts=True)[1]
            if len(num_stars) > 0:
                product_rating = num_stars[0]
            else:
                product_rating = 0

            props = {
                'name': product_name,
                'desc': product_desc,
                'imglink': product_image,
                'price': product_price,
                'rating': product_rating,
                'store': store_name
            }

            top100.append(props)

    return top100


# generate csv file from scrapped data
def make_csv(file_name, data, cols):
    df = pd.DataFrame(data, columns=cols)

    # export to csv
    df.to_csv(file_name, index=False)


# main entry point
if __name__ == '__main__':
    data = product_scrapper()
    col_names = data[0].keys()
    make_csv('tokopedia.csv', data, col_names)
