# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 16:48:35 2018

@author: Perso
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from random import randint
import json
import time
import html2text

def getContent(content):  
    
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        response = h.handle(content)
    except:
        response=""
        print("ERROR HANDLING PAGE...")
    return response


site_data = []
list_tweets=[]
tweets_id=[]
driver = webdriver.Firefox(executable_path="C:/Users/Perso/Anaconda3/selenium/webdriver/firefox/geckodriver2.exe")
url="https://twitter.com/hashtag/BalanceTonTaudis?src=hash"
driver.get(url)

html=driver.page_source
soup = BeautifulSoup(html)

for tweet in soup.findAll("li",{"class" : "js-stream-item"}):
    if(tweet["id"] not in tweets_id):
        current={}
        current["id"]= tweet["id"]
        tweets_id.append(current["id"])
        current["author"]=tweet.find("span",{"class" :"FullNameGroup"}).text
        current["account"]=tweet.find("span",{"class" :"username"}).text
        current["content"]=tweet.find("p",{"class" :"TweetTextSize"})
        list_tweets.append(current)


for t in list_tweets :
    print (t["content"])
    print(getContent(t["content"]))

with open('C:/Users/Perso/Desktop/TEST SCHOOL2/FABLABS/tweets_list.json', 'w') as outfile:
        json.dump(list_tweets, outfile)

    
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
