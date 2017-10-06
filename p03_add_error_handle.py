
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys


def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.head
    except AttributeError as e:
        return None
    return title

title = getTitle("https://www.foxplus.com/watch")
if title == None:
    print("Title could not be found")
else:
    print(title)
    
