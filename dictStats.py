#lol if you really want to me to comment this up let me know but I don't want to rn
from selenium import webdriver
import json

with open('./static/userDataDict.json') as jsonData:
    dLoad = json.load(jsonData)

haveRead = (filter(lambda item: dLoad[item][0] != "rating", dLoad))

totalLen = len(dLoad)
readLen = float(len(haveRead))

print "\nYou have read " + str(int(readLen)) + " SCPs. That's " + str(round(readLen/totalLen,3)*100) + "% of your database. "

def oneRating(ratingStr):
    print "\nYou have given these articles a rating of " + ratingStr + ": \n"
    counterNum = printForRating(ratingStr)
    print ""

    if counterNum == None:
        print "Feel free to try again lol. Exiting."
        exit
    else:
        ratedScp = (filter(lambda item: (dLoad[item][0] == ratingStr) and (len(dLoad[item]) == 5), dLoad))

        r = raw_input("Would you like to re-read one of these articles? Please enter the corresponding number to the left, or n if you'd prefer not to.\n")
        if r == "n":
            print "Kk, exiting. "
            exit
        else:
            if r in map(str,range(1,counterNum)):
                browser = webdriver.Chrome(executable_path = './static/chromedriver')
                browser.get(dLoad[ratedScp[int(r) - 1]][3])
                r0 = raw_input("Done? (y) ")
                if r0:
                    try:
                        browser.close()
                    except:
                        pass
                    oneRating(ratingStr)
            else:
                print "Error. Not a valid input. Exiting."
                exit


def printForRating(ratingStr):
    length = 5
    indexNum = length - 1

    ratedScp = (filter(lambda item: (dLoad[item][0] == ratingStr) and (len(dLoad[item]) == length), dLoad))

    titles = [dLoad[item][indexNum] for item in ratedScp]

    try:
        maxLen = len(max(titles, key=len))

        counter = 1
        for obj in ratedScp:
            title = dLoad[obj][indexNum]
            whiteSpaces = maxLen - len(title) - len(str(counter)) + 3

            strPrint = str(counter) + "." + ' ' * whiteSpaces + dLoad[obj][indexNum] + " : " + dLoad[obj][2]
            print strPrint
            counter += 1
        return counter
    except:
        print "None"

def prompt1():
    rating = raw_input("\nEnter a number to see which articles you've given this rating to. (Or enter n to exit.) ")
    if rating == "n":
        exit
    else:
        oneRating(rating)

prompt1()
