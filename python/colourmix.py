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


    def __init__(self,flag):
        self.url = "http://www.colourmix-cosmetics.com/index.php?_a=viewCat&catId=1&secat_id=1"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'referer': 'https://unwire.hk/category/'}
    def run(self):
        r = requests.get(self.url,headers=self.headers)
        soup = BeautifulSoup(r.content, "lxml")
        contentDiv = soup.find("div",{"class":"boxContent"})
        trContent = contentDiv.table.find_all("tr")

        for _tr in trContent:
            if(len(_tr.find_all("td")) != 1):
                print _tr.find_all("td")[1].text
c = colourMix("ww")
c.run()



