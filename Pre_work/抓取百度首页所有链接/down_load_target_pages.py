#############################################
## - Author: Chunlai.hua                   ##
## - Date  : 2017-10-11                    ##
## - Lang  : Python                        ##
## - Func  : Downlaod the target page      ##
#############################################


##  获取百度首页所有的超链接（link）
##  调用beautifulsoup

import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import os 

def download(url, num_retries):
    head = {}
    head['User-agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    print ("Downloading the page", url)
    try: 
        request = urllib.request.Request(url, headers=head)
        html    = urllib.request.urlopen(request).read()
    except urllib.request.URLError as e: 
        print ("Download Error:", e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, num_retries-1) 
    return html


def get_link_url(html):
    list_url = []
    link_html = open("./link.txt",'w')
    soup     = BeautifulSoup(html, 'html.parser')
    link_url = soup.find_all('a')
    print("链接网址如下：",file=link_html)
    for link in link_url:
        ## 正则过滤掉奇怪的网址
        ex_url = re.compile('java|\/$')
        if re.match(ex_url, str(link.get('href'))):
            print (link.get('href'))
        else :
            list_url.append(link.get('href'))
            link_html.write(link.get('href')+"\n")
    link_html.close
    return list_url

def getImg(items, dir_name):
    print (len(items))
    x = 1
    for imgurl in items:
        print (imgurl)
        print ("正在下载第%s张图片" %x)
        if 'https' in imgurl:
            try:
                urllib.request.urlretrieve(imgurl,'E:\python-parsing\Pre_work\抓取百度首页所有链接\%s'%dir_name + '\%s.jpg' % x)
                x+=1
            except urllib.request.URLError:
                print ("error", imgurl)
        else:
            imgurl = "https:"+ imgurl
            try:
                urllib.request.urlretrieve(imgurl,'E:\python-parsing\Pre_work\抓取百度首页所有链接\%s'%dir_name + '\%s.jpg' % x)
                x+=1
            except urllib.request.URLError:
                print ("error", imgurl)
        
url = "http://www.baidu.com"
html=download(url, 2)
list_url = get_link_url(html)
img_url_list = []

file_num = 0
for link_url in list_url:
    if "http" not in link_url:
        link_url = "https:" + link_url
    file_num+=1
    file_name = './' + str(file_num) + '_src'
    print ("The link url is : ", link_url)
    os.mkdir(file_name)
    html=download(link_url, 2)
    soup     = BeautifulSoup(html, 'html.parser')
    link_url = soup.find_all('img')
    for img_url in link_url:
        url = img_url.get('src')
        img_url_list.append(url)
        getImg(img_url_list, file_name)







