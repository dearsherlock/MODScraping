from urllib.request import urlopen
from bs4 import BeautifulSoup
html=urlopen("https://www.foxplus.com/watch")
bsObj=BeautifulSoup(html.read())
print(bsObj.head)