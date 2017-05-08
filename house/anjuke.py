# coding:utf-8
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

data_file = open('data_anjuke.csv', 'w+')

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

def get_random_proxies():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    return get_random_ip(ip_list)

# 过滤存在的城市名称
unique_citys = []
def extract_new(url):
    url = url.replace('anjuke.com', 'fang.anjuke.com/loupan/s?kw=' + urllib.quote('恒大'))
    print 'extract : ', url
    try :
        doc = pyq(url=url)
        cts = doc('.list-contents>.list-results>.key-list>.item-mod')
        city = doc(".city").text()
        if city in unique_citys :
            print 'city ' + city + ' 已经抓取过'
            return
        unique_citys.append(city)
        for i in cts:
            name = cts(i).find('.infos h3 .items-name').text().strip()
            html = cts(i).find(".favor-pos>.price").html()
            if html == None :
                html = cts(i).find(".favor-pos .around-price").html()
                price = ''
                unit = ''
                if html == None :
                    content = ''
                    referto_price = ''
                    referto_unit = ''
                else :
                    content = cts(i).find(".favor-pos .around-price").text().strip()
                    referto_price = cts(i).find(".favor-pos .around-price>span").text().strip()
                    referto_unit = html[html.index('</span>') + 7:].strip()
            else :
                price = cts(i).find(".favor-pos .price>span").text().strip()
                unit = html[html.index('</span>') + 7:].strip()
                content = cts(i).find(".favor-pos>.price").text().strip()
                referto_price = ''
                referto_unit = ''
            data_file.write(city + '\t' + name + '\t' + price + '\t' + unit + '\t' + content + '\t' + referto_price + '\t' + referto_unit + '\n')
            data_file.flush()
    except Exception, e:
        print e

proxies = get_random_proxies()
def extract(url, page=None):
    print ''
    key = '恒大'
    if page :
        _url = url + '/community/p' + str(page) + '/?kw=' + urllib.quote(key)
    else :
        _url = url + '/community/?kw=' + urllib.quote(key)
        page = 1
    print 'extract : ', _url
    try :
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        data = requests.get(_url, headers=headers)
        doc = pyq(data.text)
        city = doc("#switch_apf_id_5").html().strip()
        city = city.split('<')[0]
        city_key = city + str(page)
        print city_key
        if city_key in unique_citys :
            print 'city_key ' + city_key + ' 已经抓取过'
            return
        unique_citys.append(city_key)
        cts = doc('#list-content>.li-itemmod')
        total = 0
        if cts:
            for i in cts:
                name = cts(i).find('.li-info>h3>a').text().strip()
                if key not in name:
                    print 'filter ~ ' + name
                    continue
                text = cts(i).find(".li-side>p").eq(0).text().strip()
                arr = text.split(" ")
                if len(arr) == 1:
                    price = arr[0]
                    unit = arr[0]
                else:
                    price = arr[0]
                    unit = arr[1]
                content = cts(i).find(".li-side>p").html().strip()
                referto_price = ''
                referto_unit = ''
                data_file.write(city + '\t' + name + '\t' + price + '\t' + unit + '\t' + content + '\t' + referto_price + '\t' + referto_unit + '\n')
                data_file.flush()
                total = total + 1
        print city + ' 第' + str(page) + '页 有 ' + str(total) + ' 条数据。'
        page_size = len(doc('.page-content>.multi-page').children()) - 3
        if page_size >= page :
            sleep(5)
            extract(url, page=page + 1)
    except Exception, e:
        print str(Exception)
        print str(e)

if __name__ == '__main__':
    file_object = open('url_anjuke.csv')
    i = 0
    for line in file_object:
        print i
        url = line.replace('\n', '')
        extract(url)
        i = i + 1
        sleep(60 * 1)
#     extract('http://anshan.anjuke.com')
#     extract('http://bengbu.anjuke.com')
#     extract('http://shanghai.anjuke.com')







