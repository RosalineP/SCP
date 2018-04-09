from bs4 import BeautifulSoup
import requests
import json
import csv
from selenium import webdriver
import random

#order of value-list in the dictionary, for each article: rating, read, blurb, url, name

with open('./static/userDataDict.json') as jsonData:
    dLoad = json.load(jsonData)

#create dict of unread SCPs
unread = {key: dLoad[key] for key in dLoad if str(dLoad[key][1]) != "true"}
key = random.choice(unread.keys())

scp = dLoad[key][3]
print ("Here's a random SCP! \n" + dLoad[key][4])

#fetch appropriate page
browser = webdriver.Chrome(executable_path = './static/chromedriver')
browser.get(scp)

#respond to user input
r0 = raw_input("Read, y/n? ")
if r0 == "n":
    print ("Kk, closing article.")
    try:
        browser.close()
    except:
        pass
    exit
if r0 == "y":
    ra = raw_input("Rating? ")
    dLoad[key][0] = ra
    rb = raw_input("Blurb? ")
    dLoad[key][2] = rb
    dLoad[key][1] = "true"
    print("Save successful.")
    try:
        browser.close()
    except:
        pass

#update userDataDict with new info
with open('./static/userDataDict.json', 'w') as fp:
    json.dump(dLoad, fp)
