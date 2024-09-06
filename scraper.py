import requests
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import csv
# from app import db, Book
# from db import engine, Book



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
    # returns all prices that are indicated on page as "from"
    # (can't go with css selector because there's no tag, just a string value sandwiched between two tags)
    prices = dom.xpath('//span[@class="olp-from"]/following::text()')
    # strip the pound signs and convert prices to floats for comparison
    #float_prices = [float(price.strip()[1:]) for price in prices]
    #return min(float_prices)
    # the error seemed to be that min() was called on an empty item, but the xpath expression seems to work
    # so trying if returning the element directly works
    if type(prices) is not list:
        return float(prices.strip()[1:])
    float_prices = []
    for price in prices:
        try:
            if float(price.strip()[1:]) != 0.0:
                float_prices.append(float(price.strip()[1:]))
        except:
            continue
    #return [float(price.strip()[1:]) for price in prices if price != ""]
    return min(float_prices)

""" Session = sessionmaker(bind=engine)
session = Session() """


