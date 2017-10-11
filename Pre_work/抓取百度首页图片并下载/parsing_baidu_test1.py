#############################################
## - Author: Chunlai.hua                   ##
## - Date  : 2017-10-10                    ##
## - Lang  : Python                        ##
## - Func  : Downlaod the target page      ##
#############################################


## <1> 重试下载功能
## <2> 设置用户代理
## <3> 下载目标网页 


from bs4 import BeautifulSoup
import urllib
import urllib.request
import re

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

## ---- belwo content just for test ## 
f     = open("./html", "wb") 
url1  = "http://www.baidu.com"
html  = download(url1,2)
f.write(html)
f.close


##---- 获取百度首页logo图片 ----##

## 正则抓取
html = html.decode('utf-8')
img = re.findall('<img.*?src="(.*?)".*?>',html)

def getImg(items):
    print (len(items))
    x = 1
    for imgurl in items:
        print (imgurl)
        print ("正在下载第%s张图片" %x)
        if 'https' in imgurl:
            try:
                urllib.request.urlretrieve(imgurl,'%s.jpg' % x)
                x+=1
            except urllib.request.URLError:
                print ("error", imgurl)
        else:
            imgurl = "https:"+ imgurl
            try:
                urllib.request.urlretrieve(imgurl,'%s.jpg' % x)
                x+=1
            except urllib.request.URLError:
                print ("error", imgurl)
getImg(img)

