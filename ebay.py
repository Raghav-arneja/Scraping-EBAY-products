import pandas as pd 
import requests 
from requests.compat import quote_plus
from bs4 import BeautifulSoup

Base_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw={}&_sacat=0&_pgn=1'
search = input('enter the item to search :')
Mixing_url = Base_url.format(quote_plus(search))
Final_url = requests.get(Mixing_url)
# print(Mixing_url)
print(Final_url)
global title,  price, image
title = []
price = []
product_url = []
product_image_url = []
soup = BeautifulSoup(Final_url.content, 'html.parser')

# extracting the data
def scrape_data(pass_soup):
    # get_url = requests.get(url)
    # soup = BeautifulSoup(get_url.content, 'html.parser')

    results = pass_soup.find(id="srp-river-results")

    product_list = results.find_all(class_ = 's-item')
    for item in product_list:
        title_text = item.find(class_ = 's-item__title').get_text()
        price_text = item.find(class_ = 's-item__price').get_text()
        item_url = item.find('a').get('href')
        image_url = item.find('img')['src']

        title.append(title_text)
        price.append(price_text)
        product_url.append(item_url)
        product_image_url.append(image_url)
    # print(len(title))
    
scrape_data(soup)

pages = soup.find(class_ = 'pagination__items')
print(len(pages))
links = pages.find_all('a')
# print(links)
for link in links:
    href= link.get('href')

    if (href == Mixing_url):
        print('ye scrape nhi hoga')
        continue
    else:
        other_url = requests.get(href)
        print(other_url)
        soup1 = BeautifulSoup(other_url.content, 'html.parser')
        scrape_data(soup1)

product_items = pd.DataFrame({
    'title' : title,
    'price' : price,
    'product_url': product_url,
    'image_url' : product_image_url,
})

product_items.to_csv('Ebay_product_list.csv')