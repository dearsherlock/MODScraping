
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys
import re

class MovieInfo:
	"""docstring for ClassName"""
	def __init__(self, category,title,description,path, actors,license,id,link,poster,offlineDate):
		self.category=category
		self.title = title
		self.description = description		
		self.path = path
		self.actors = actors
		self.license = license
		self.id = id
		self.link = link
		self.poster = poster
		self.offlineDate=offlineDate
	def __str__(self):
		return "MovieInfo({0}, {1}, {2},{3},{4},{5},{6},{7},{8},{9})".format(self.title, self.description, self.path,self.actors,self.license,self.id,self.link,self.poster,self.offlineDate,self.category)

def getMovieDetails(path,movieInfo):
    try:
        html = urlopen(path)
    except HTTPError as e:
        print(e)
        return None
    try:

#LICENSE <i class="video-info-list__path" style="background-color:#0066CC;color:#fff;">多螢</i>
#Actors <span class="video-info-list__content">徐熙娣,林志玲,金世佳</span>
        bsObj = BeautifulSoup(html.read(),"html5lib")
        valuelicense=bsObj.find("i",{"class":"video-info-list__path"})
        valueActors=bsObj.findAll("span",{"class":"video-info-list__content"})[2]
        offlineDate=bsObj.findAll("span",{"class":"video-info-list__content"})[3]

        expopath=bsObj.findAll("span",{"class":"video-info-list__content"})[1]
#        print("--"+bsObj.findAll("span",{"class":"video-info-list__content"})[1].find("span",{"class":"video-info-list__content"}))
        subpathAll=""
        for subpath in expopath.children:
        	subpathAll = subpath.get_text() + " " + subpathAll
        description=bsObj.find("p",	{"class":"info-data-card__summary"}).get_text()

        movieInfo.license=valuelicense.get_text()
        movieInfo.actors=valueActors.get_text()
        movieInfo.offlineDate=offlineDate.get_text()
        movieInfo.path=subpathAll
        movieInfo.description=description	
        	
    except AttributeError as e:
        print (e)
        return None
    return movieInfo


def getMoviesInCategory(categoryName,category,title,dictMovies):
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
        	
        	movieInfo=MovieInfo(categoryName,"","","","","","","","","")
        	titleS=name.get_text()
        	movieInfo.title=titleS
        	movieInfo.link="http://mod.cht.com.tw"+ name.parent.parent.parent.find("a",{"class":"port-card__inner"})['href']
        	movieInfo.poster="http://mod.cht.com.tw"+ name.parent.find("img")['src']
        	boolHasKey=dictMovies.__contains__(titleS)
        	if boolHasKey==True:
        		print ("skiping")
        		continue
        	movieInfo=getMovieDetails(movieInfo.link,movieInfo)
        	print (movieInfo)
        	dictMovies[titleS]=movieInfo
        	
    except AttributeError as e:
        return None
    return len(valueC)

def getCategory(title,url):
    dictMovies={}
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
        	totalCount=totalCount+getMoviesInCategory(title,name["href"],name.get_text(),dictMovies)
        print( title+"total have movies count="+str(totalCount)+",after filter is "+str( len(dictMovies)  ))
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
    
