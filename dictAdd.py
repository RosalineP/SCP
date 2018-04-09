import json
import csv

with open('./static/userDataDict.json') as jsonData:
    dLoad = json.load(jsonData)

with open('./static/names.json') as jsonData:
    names = json.load(jsonData)

def nameFinder(r):
    try:
        return names[r[4:]]
    except:
        return "(Title not found)"


r = raw_input("Would you like to 1. Add an SCP you haven't read yet or 2. Add an SCP you've already read? (Enter 1 or 2.) \n")
base = "http://www.scp-wiki.net/"
if r == "1":
    a = raw_input("\nPlease enter the url end of the article in question.\n")
    key = "['/"+ a +"']"
    dLoad[key] = ("rating","read","blurb",base+a,nameFinder(a))
    print "Successfully added."
elif r == "2":
    a = raw_input("\nUrl end: ")
    b = raw_input("Your rating: ")
    c = raw_input("Your blurb: ")

    key = "['/"+ a +"']"

    dLoad[key] = (b,"true",c,base+a,nameFinder(a))
    print "Successfully added."

else:
    print "That was not 1 or 2, man. Exiting."



with open('./static/userDataDict.json', 'w') as fp:
    json.dump(dLoad, fp)
