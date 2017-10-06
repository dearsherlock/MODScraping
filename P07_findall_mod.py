
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys
import re

def getMoviesInCategory(category,title):
    try:
        html = urlopen("http://mod.cht.com.tw"+category)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        valueC=bsObj.findAll("h5",{"class":re.compile("port-card__heading")})
        #print(valueC)

        for name in valueC:
        	
        	print("電影199 Directory "+title+" movie:"+name.get_text())
    except AttributeError as e:
        return None
    return len(valueC)

def getCategory(title,url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        valueC=bsObj.findAll("a",{"class":re.compile("video-area__heading-link")})
        #print(valueC)
        totalCount=0
        for name in valueC:        	
        	print(title+"Directory:"+name.get_text()+"  "+name["href"])
        	totalCount=totalCount+getMoviesInCategory(name["href"],name.get_text())
        print( title+"total have movies count="+str(totalCount))
    except AttributeError as e:
        return None
    return "OK"
#電影199  http://mod.cht.com.tw/video/set_monthly.php?id=1
#好萊塢199  http://mod.cht.com.tw/video/set_monthly.php?id=2
title = getCategory("電影199 ","http://mod.cht.com.tw/video/set_monthly.php?id=1")

if title == None:
    print("Title could not be found")
else:
    print(title)
    
