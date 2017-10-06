
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
        bsObj = BeautifulSoup(html.read())
        categorys = bsObj.findAll("span",{"class","author-label"})
        print(len(categorys))
        for name in categorys:
        	print("Hello")
        	print(name.get_text())
    except AttributeError as e:
        return None
    return "OK"

title = getCategory("http://dearsherlock.github.io/travel/hongkong-day5")
if title == None:
    print("Title could not be found")
else:
    print(title)
    
