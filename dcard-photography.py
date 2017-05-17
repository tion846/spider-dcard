# -*- coding: UTF-8 -*-
# "#表示註解"
import urllib.request
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup #import BeautifulSoup

#第一步:
# HTML資料
url = "https://www.dcard.tw/f/photography" #爬取的目標網址
websiteUrl =[] #陣列 存放要抓圖片的文章網址

#設置假的瀏覽器資訊 (有些網頁會拒絕機器訪問，headers可以模擬瀏覽器環境)
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
#發送請求
req = urllib.request.Request(url = url,headers=headers)  #需要 import urllib.request
page = urllib.request.urlopen(req) #urlopen 嗯...打開網頁
contentBytes = page.read() #將抓到的網頁原碼存放在contentBytes (type=byte)

soup = BeautifulSoup(str(contentBytes), "html.parser") #需要 from bs4 import BeautifulSoup
#透過BeautifulSoup 解析contentBytes ，並存在soup


arr = soup.find_all("a", { "class" : "PostEntry_entry_2rsgm"},limit=10)
# find_all()  找到所有
# "a" 抓 <a>
# 篩選<a>的class = PostEntry_entry_2rsgm
#limit=10 可以控制數量，表示前10個PO文

#將爬到的<a>個別拆解，抓<a>的href
for aTag in arr:
    article = BeautifulSoup(str(aTag), "lxml")
    aUrl = 'https://www.dcard.tw' + article.a.attrs['href'][0:26]
    # str[0:26]表示擷取0到第26個
    # dcard會把標題放在網址，不過前面的9位數字即可讀取該網頁
    # 爬取不同版，要修改一下[0:i]
    websiteUrl.append(aUrl)
    # array.append(item) 表示將item加入array (python裡的陣列叫做list)
    print(aUrl)
    #印出每個網址

print("\n")
#空行


#第二步:
#訪問每篇文章
for webUrl in websiteUrl:
    url = webUrl
    req = urllib.request.Request(url = url,headers=headers)
    page = urllib.request.urlopen(req)
    contentBytes = page.read()

    try:contentBytes = contentBytes.decode('UTF-8')
    except (urllib.HTTPError,e):
        print(e.contentBytes)
    #contentBytes是抓下來的原碼，無法閱讀
    #透過byte.decode('UTF-8')轉換成文字
    
    dSoup = BeautifulSoup(str(contentBytes), "html.parser")
    title = dSoup.title.text
    #dSoup.title.text 抓<title>裡的text
    
    print(title) #標題有Emoji表情符號不能用UTF-8輸出，會出錯
    #爬西斯版要注意T T

    picturesTag = dSoup.find_all("img",{"class":"GalleryImage_image_3lGzO"})
    #抓到全部 帶有class=GalleryImage_image_3lGzO 的 <img> 

    path = './dcard-photography/'+title+'/' #存放位置，依照title建立資料夾
    
    if not os.path.exists(path): #檢查資料夾是否存在 需要import os
        os.makedirs(path)        #不存在就建立
    
    for pic in picturesTag :
        
        pSoup = BeautifulSoup(str(pic),"lxml")
        picUrl = pSoup.find("img").attrs['src']
        #抓<img>裡的src
        # picUrl存放圖片網址
        fileName = picUrl[23:]
        # fileName檔案名稱 
        print(picUrl,fileName) #印出來檢查一下
                
#第三步:
#下載圖片
#dcard圖片比較嚴謹，需要headers才能訪問下載
        url = picUrl
        req = urllib.request.Request(url = url,headers=headers)
        img = urllib.request.urlopen(req)
        
        with open(path+fileName, 'wb') as f:
            f.write(img.read())
        #open(存放位置 , 'wb'是甚麼，我不知道T T )


