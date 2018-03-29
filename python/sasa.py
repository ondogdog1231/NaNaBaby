# coding=utf-8
import threading
import requests
import re
import time
import datetime
from datetime import datetime
import hashlib
from tabulate import tabulate
from bs4 import BeautifulSoup
from contextlib import closing
from pprint import pprint
import sys
import json
from random import randint

import string
import random

reload(sys)
sys.setdefaultencoding('utf8')


class sasa():
    totalThread = 0
    resultList = []

    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'referer': 'http://www.colourmix-cosmetics.com/'
        }
        self.data = []

    def run(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.content, "lxml")
        contentDiv = soup.find("div", {"class": "product-list"})
        if contentDiv is None:
            return False
        if contentDiv.find_all("product-col") is None:
            return False
        productList = contentDiv.find_all("div", {"class": "product-col"})

        for _div in productList:
            brand = _div.find("div", {"class": "product-manufacturer"}).text.strip()
            product = _div.find("div", {"class", "item_name"}).text.strip()
            price = _div.price.text
            link = _div.find("div", {"class", "image"}).a["href"]
            photo = _div.find("div", {"class", "image"}).img["src"]
            self.data.append({
                "brand": brand,
                "name": product,
                "price": price,
                "link": link,
                "photo": photo
            })
        return self.data


dataJson = {}
dataJson["products"] = []
categories = {
    "skincare": 38,
    "makeup": 11,
    "bodyhealth": 2,
    "fragrance": 2,
    "personalcare": 9,
    "formen": 2
}

for categories, page in categories.iteritems():
    print categories
    page = page + 1
    for i in range(0, page):
        c = sasa("https://www.bonjourhk.com/" + categories + "?page=" + str(i))
        dataDict = c.run()
        if dataDict is False:
            break
        for _data in dataDict:
            print _data["name"] + " " + str(_data["price"])

            dataJson["products"].append(_data)
        print "page " + str(i) + "grab finished"
        time.sleep(1)
# print dataJson
# print json.dumps(dataJson,encoding='UTF-8', ensure_ascii=False)
with open('../json/sasa.json', 'a') as outfile:
    json.dump(dataJson, outfile, encoding='UTF-8', ensure_ascii=False)
