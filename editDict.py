from bs4 import BeautifulSoup
import requests
import json
import csv
from selenium import webdriver
import random



with open('./static/userDataDict.json') as jsonData:
    dLoad = json.load(jsonData)

r0 = raw_input("Please enter the final URL segment of the article you wish to change.\n")

try:
    key = "['/" + r0 + "']"
    article = dLoad[key]
    print "\nArticle found. \n"

    print "Rating: " + ("Unrated" if str(article[0]) == "rating" else str(article[0]))
    print "Blurb: " + ("Unwritten" if str(article[2]) == "rating" else str(article[2]))
    print "Title: " + article[4]

    r1 = raw_input("\nPlease enter the new rating, blurb, and title of this article. \nUse commas to delineate fields. \nOr, enter 'n' to cancel and exit program.\n")
    if r1 == 'n':
        exit
    else:
        info = r1.split(',')
        try:
            dLoad[key] = [info[0],"true",info[1],dLoad[key][3],info[2]]
            print("\nSuccess")
            with open('./static/userDataDict.json', 'w') as fp:
                json.dump(dLoad, fp)
        except IndexError:
            print "There was an error with what you just entered. Please try again, like, more carefully. Exiting."
            exit





except KeyError:
    print "That is not a valid final URL segment."
    exit
