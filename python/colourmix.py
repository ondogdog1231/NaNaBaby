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


class colourMix():
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
        contentDiv = soup.find("div", {"class": "boxContent"})
        if contentDiv is None:
            return False
        if contentDiv.table is None:
            return False
        trContent = contentDiv.table.find_all("tr")
        if trContent is None:
            return False
        for _tr in trContent:
            if (len(_tr.find_all("td")) != 1):
                brand = _tr.find_all("td")[1].find_all("a")[0].text.strip()
                product = _tr.find_all("td")[1].find_all("a")[1].text.strip() + " " + \
                          _tr.find_all("td")[1].find_all("a")[2].text.strip()
                link = "http://www.colourmix-cosmetics.com/" + _tr.find_all("td")[1].find_all("a")[1]["href"]
                rePrice = re.search(r"[0-9,]+(\.[0-9]{2})",
                                    _tr.find_all("td")[2].find("span", {"class": "str_price"}).text)
                if rePrice:
                    price = rePrice.group()
                else:
                    price = None
                photo = None
                rawPhoto = _tr.find_all("td")[0].find("img")
                if rawPhoto is None:
                    return False
                photo = rawPhoto["src"].replace("thumbs/thumb_","")



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
    "Female": "1",
    "Male": "152"
}


for categories, catId in categories.iteritems():
    print categories
    for i in range(0, 120):
        c = colourMix("http://www.colourmix-cosmetics.com/index.php?_a=viewCat&catId="+catId+"&secat_id="+catId+"&page="+ str(i))
        dataDict = c.run()
        if dataDict is False:
            break
        for _data in dataDict:
            print _data["name"] + " " + str(_data["price"])
            dataJson["products"].append(_data)
        print "page " + str(i) + "grab finished"
    time.sleep(5)
# print dataJson
with open('../data5.json', 'a') as outfile:
    json.dump(dataJson, outfile, encoding='UTF-8', ensure_ascii=False)
