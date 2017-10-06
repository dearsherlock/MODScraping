
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import sys
import re
import csv
import codecs
from datetime import date
import time
class MovieInfo:
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

def saveCsv(title,filepath,dictMovies):
	updateTime=str(date.today())+" "+str(time.strftime("%H:%M:%S"))
	with open(filepath+title+".csv",'w',newline='',encoding='utf-8-sig') as csvFile:

		write=csv.writer(csvFile)
		write.writerow([u'產品包裝',u'名稱',u'下片日期',u'目錄路徑',
			u'簡介',	u'演員',	u'授權',	u'連結',	
			u'圖片',u'更新日期'])
		for item in dictMovies.keys():
			eachMovieInfo=dictMovies[item]

			write.writerow((eachMovieInfo.category,eachMovieInfo.title,eachMovieInfo.offlineDate,eachMovieInfo.path,
				eachMovieInfo.description,eachMovieInfo.actors,eachMovieInfo.license,eachMovieInfo.link,
				eachMovieInfo.poster,updateTime))

		csvFile.close()


def getMovieDetails(path,movieInfo):
    try:
        html = urlopen(path)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html5lib")
        subpathAll=""
        valueActors=""
        offlineDate=""
        valuelicense=""

        for subV in bsObj.findAll("li",{"class":"video-info-list__item"}):
            if subV.find("span",{"class","video-info-list__title"}):
                if "目錄路徑" in subV.get_text():
                    expopaths=subV.findAll("i",{"class","video-info-list__path"})
                    subpathAll=""
                    for subpath in expopaths:
                        subpathAll = subpath.get_text() + " " + subpathAll
                if "演員" in subV.get_text():
                    valueActors=subV.find("span",{"class","video-info-list__content"}).get_text()
                if "下片日期" in subV.get_text():
                    offlineDate=subV.find("span",{"class","video-info-list__content"}).get_text()
            else:
                #多螢標籤，有內容沒有Title
                valuelicense=subV.find("span",{"class","video-info-list__content"}).get_text()
        description=bsObj.find("p",	{"class":"info-data-card__summary"}).get_text()

        movieInfo.license=valuelicense
        movieInfo.actors=valueActors
        movieInfo.offlineDate=offlineDate
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

        for name in valueC:
        	
        	movieInfo=MovieInfo(categoryName,"","","","","","","","","")
        	titleS=name.get_text()
        	movieInfo.title=titleS
        	movieInfo.link="http://mod.cht.com.tw"+ name.parent.parent.parent.find("a",{"class":"port-card__inner"})['href']
        	movieInfo.poster="http://mod.cht.com.tw"+ name.parent.find("img")['src']
        	boolHasKey=dictMovies.__contains__(titleS)
        	if boolHasKey==True:
        		continue
        	movieInfo=getMovieDetails(movieInfo.link,movieInfo)
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
        totalCount=0
        for name in valueC:        	
        	print(title+"Directory:"+name.get_text()+"  "+name["href"])
        	totalCount=totalCount+getMoviesInCategory(title,name["href"],name.get_text(),dictMovies)
        print( title+"total have movies count="+str(totalCount)+",after filter is "+str( len(dictMovies)  ))
        saveCsv(title,"",dictMovies)
    except AttributeError as e:
        print (e)
        return None
    return "OK"


def getMOD(type,url):
	result = getCategory(type,url)
	if result == None:
		print("Title could not be found")
	else:
		print(result)

getMOD("電影199","http://mod.cht.com.tw/video/set_monthly.php?id=1")
getMOD("好萊塢199","http://mod.cht.com.tw/video/set_monthly.php?id=2")
getMOD("單點電影","http://mod.cht.com.tw/video/set.php?id=17")
getMOD("戲劇199","http://mod.cht.com.tw/video/set_monthly.php?id=3")
getMOD("卡通199-兒童","http://mod.cht.com.tw/video/set_monthly.php?id=4")
getMOD("卡通199-動漫","http://mod.cht.com.tw/video/set_monthly.php?id=5")
getMOD("紀實149","http://mod.cht.com.tw/video/set_monthly.php?id=7")