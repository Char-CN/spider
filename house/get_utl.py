# coding=utf-8
'''
Created on 2017年5月8日

@author: hyy
'''
import urllib
import urllib2
from pyquery import PyQuery as pyq
from time import sleep

from bs4 import BeautifulSoup
import requests
import random
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 过滤存在的城市名称
unique_citys = []
def get_anjuke(url, file_name):
    data_file = open(file_name, 'w+')
    try :
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        data = requests.get(url, headers=headers)
        doc = pyq(data.text)
        all_a = doc.find('#content>.cities_boxer a')
        for i in all_a:
            href = all_a(i).attr('href')
            if href in unique_citys :
                continue
            data_file.write(href + '\n')
            data_file.flush()
            unique_citys.append(href)
    except Exception, e:
        print str(Exception)
        print str(e)

if __name__ == '__main__':
    get_anjuke('http://www.anjuke.com/sy-city.html', 'url_anjuke.csv')











