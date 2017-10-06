
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys


def getCategory(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        categorys = bsObj.body#.find("div",{"id","react-root"})
        #print(categorys)
        valueC=bsObj.find("div",{"id":"react-root"})
        print(valueC)
        return 1
        for name in categorys:
        	print("Hello")
        	print(name.get_text())
    except AttributeError as e:
        return None
    return "OK"

title = getCategory("https://www.foxplus.com/watch")
if title == None:
    print("Title could not be found")
else:
    print(title)
    
