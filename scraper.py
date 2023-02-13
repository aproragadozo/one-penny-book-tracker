import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import csv

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

wish_list = ["https://www.amazon.co.uk/dp/0091958482",
"https://www.amazon.co.uk/gp/product/0137058268",
"https://www.amazon.co.uk/dp/140520625X",
"https://www.amazon.co.uk/gp/product/1405206306"]

def get_price(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.content, "html.parser")
    dom = et.HTML(str(soup))
    price = dom.xpath('//span[@class="olp-from"]/following::text()')[0]
    return float(price.strip()[1:])

# price = float(dom.xpath('//span[@class="olp-from"]/following::text()')[0].strip()[1:])
# print(price)

for item in wish_list:
    print(get_price(item))