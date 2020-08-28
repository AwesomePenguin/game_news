# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 00:07:11 2020

@author: sihan

Video game news push from Tgbus
"""

import requests
from bs4 import BeautifulSoup 
from win10toast import ToastNotifier
import os
import pandas as pd
import schedule
import time

path = 'app/download' if os.path.isdir('app/download') else 'download'
icon = 'app/data/tgbus.ico' if os.path.isdir('app/data') else 'data/tgbus.ico'
if not os.path.isdir(path):
    os.mkdir(path)
file_path = os.path.join(path, 'news_links.xlsx')

toast = ToastNotifier()

URL = "http://www.tgbus.com/list/yaowen/"

def run():
    print('Checking news...')
    if os.path.exists(file_path):
        news = pd.read_excel(file_path, usecols=['headline','subline','link','time'])
    else:
        news = pd.DataFrame()
    
    news_list = []
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('div', attrs = {'class':'list-zone__article common__shadow--dark-h'})
    
    for row in table.findAll('div', attrs = {'class':'information-item'}):
        item = {}
        link = row.a['href']
        if len(news) == 0 or not link in list(news['link']):
            item['headline'] = row.find('div', attrs = {'class':'information-item__content-top'}).h4.text
            item['subline'] = row.find('div', attrs = {'class':'information-item__content-top'}).p.text
            item['link'] = link
            item['time'] = row.find('span', attrs = {'class':'information-item__date'}).text
            news_list.append(item)
            toast.show_toast(item['headline'], item['subline'], icon_path=icon, duration=5)
        
    news_df = pd.DataFrame(news_list, columns=['headline','subline','link','time'])
    news = news.append(news_df)
    news.to_excel(file_path)
    print('Done checking...')
    
schedule.every().hour.do(run)
print('Going to sleep...')

while 1:
    schedule.run_pending()
    time.sleep(1)