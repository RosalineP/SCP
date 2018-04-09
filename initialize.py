from bs4 import BeautifulSoup
import requests
import json
import csv
from selenium import webdriver
import random


#from a 'top rated' page, returns url ends for the linked articles/tales on that page
def getUrlEnds(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    mydivs = soup.findAll("div", {"class" : "list-pages-box" })
    hrefList = []

    for item in mydivs[1]:
        for thing in (str(item).split('\n')):
            hrefList.append(thing)

    urlEnds = []
    for thing in hrefList[2:(len(hrefList)-5)]:
        urlEnds.append(thing.split('"')[1])
    return urlEnds

#from all six 'top rated' pages, collect all url ends
def collectAllPages(url):
    allUrlEnds = getUrlEnds(url)
    pgNum = 2
    while pgNum < 7:
        currentPage = url + "/p/" + str(pgNum)
        allUrlEnds += getUrlEnds(currentPage)
        pgNum += 1
    return allUrlEnds


#write all of the scpUrlEnds into a csv file for later processing,
#eliminating need to re-crawl for the scpUrlEnds for further computations
url = "http://www.scp-wiki.net/top-rated-pages"
with open('./static/scpUrlEnds.csv','wb') as file:
    for value in collectAllPages(url):
        file.write(value)
        file.write('\n')



d = {}
#create names.json
#From the SCP series page, create tuples of form ['SCP designation number', 'sub-title'],
#and add each to d
def getNames(url,isFirst):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    l = []
    for li in soup.findAll('li'):
        l.append(str(li))

    cutoff = [27,30]
    if not isFirst:
        cutoff = [18,22]

    for item in l[264:len(l)-8]:
        t1 = item[cutoff[0]:cutoff[1]]
        thing = item.split('</a>')[1]
        t2 = thing[3:len(thing)-5]
        if (t2 == "[ACCESS DENIED]"):
            continue
        global tups
        global d
        d[t1] = t2

getNames("http://www.scp-wiki.net/scp-series", True)
getNames("http://www.scp-wiki.net/scp-series-2", False)
getNames("http://www.scp-wiki.net/scp-series-3", False)
getNames("http://www.scp-wiki.net/scp-series-4", False)
with open('./static/names.json', 'w') as fp:
    json.dump(d, fp)


#for creating userDataDict.json, which contains dict of SCPs and user-entered ratings, blurbs, etc
#weaves information from scpUrlEnds.csv, and names.json
#the dictionary userDataDict is of the form {[url-end] : [rating, read-or-not-bool, blurb, full url, ]  }
def createBigDict():
    base = "http://www.scp-wiki.net"
    d = {}
    def searchName(num):
        #finds the sub-title of an SCP mainlist article
        with open('./static/names.json') as jsonData:
            dLoad = json.load(jsonData)
            if not (str(num) in dLoad):
                return None
            return dLoad[str(num)]

    with open('./static/scpUrlEnds.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            r = str(row)[2:len(row)-3]

            name = None
            #testing whether article in question is in mainlist
            if r[5:].isdigit():
                name = str(r[5:])

            if not name:
                nameTale = str(row)[3:len(row)-3].replace('-',' ')
                d[str(row)] = ("rating","read","blurb",base+r,nameTale)
            if name:
                scpName = searchName(name)
                if not (scpName == None):
                    name = "SCP-" + name + ": " + scpName
                d[str(row)] = ("rating","read","blurb",base+r,name)
    return d

createBigDict()

with open('./static/userDataDict.json', 'w') as fp:
    json.dump(createBigDict(), fp)
