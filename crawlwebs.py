'''
Scrape the page link of each company in a single page
'''

#request.get方法：获取url
from requests import get
from bs4 import BeautifulSoup
import urllib.parse
import re

#time.sleep（seconds)方法：延迟操作几秒时间
from time import sleep
#random.randint()方法：随机生成一个Int类型，可以指定整数范围
from random import randint
#time.time()返回当前时间的时间戳
from time import time

#csv模块是常用的文本格式，用以储存表格数据
import csv


start_time = time()
requests = 0

totalpages = 76

pages = [str(i) for i in range(1,totalpages+1)]

# ----------------get the company link for all pages-------------------------------------------

companylinks = []
for page in pages:  # the loop for 76 pages of companies

    url = 'https://www.siww.com.sg/exhibitor?page='+page
    
    response = get(url)

    #--------(not important things) to avoid crushing the website server--------   
    # pause for a while for each page
    sleep(randint(1,2))
    requests += 1
    elapsed_time = time() - start_time
    #format内置函数作用：格式化字符串
    print('Page:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    
    if response.status_code != 200:
        print('warning: request too frequent...')
    #---------------------------------------------------------------------------
  
    html_soup = BeautifulSoup(response.text, 'html.parser')
    
    #---parser the content
    card_containers = html_soup.find_all('div', class_ = 'card-content')
    
    for companycard in card_containers:
        #通过后缀.a获取tag是a的内容
        sublink = companycard.a
        link = urllib.parse.urljoin("https://www.siww.com.sg", sublink['href'])
        companylinks.append(link)
    
# ------Find the contents we need for each companylink--------------------------------------

name = []
web = []
booth = []
des = []
requests = 0
for url in companylinks:
    requests += 1
    print(requests)
    try:
        response = get(url)
        sleep(randint(1,2))
        html_soup = BeautifulSoup(response.text, 'html.parser')
    # name
        right_column = html_soup.find('div', class_ = "right-column").find('h2')
        name.append(right_column.get_text(strip = True))
    
    # web
        web_node = html_soup.find('div', class_ = 'button-container')
        web.append(web_node.a['href'])
    
    # booth 
        booth_node = html_soup.find('span', class_ = "booth-info--no")
        booth.append(booth_node.get_text(strip = True))
    
    # desription
        des_node = html_soup.find('div', class_ = "bottom-row").find('p')
        des.append(des_node.get_text(strip = True))

    except Exception as e:
        print(str(e))

# -------output------------------------------------------------------------------------------

data = [name,booth,web, des]  
#open方法打开一个csv表格文件，第一个参数output.csv给文件命名，第二个参数'w'表示写
# encode表示将unicode转化为csv识别的utf-8，newline去掉空白行
myFile = open('jingijng3.csv', 'w', encoding="utf-8",newline='')

with myFile:  
   #csv.writer()方法
   writer = csv.writer(myFile)
   #若代码为writer.writerows(data),输出的csv文件行和列相反
   writer.writerows(zip(*data))



