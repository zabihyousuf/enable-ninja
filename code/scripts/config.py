# Import libraries
from html.parser import HTMLParser
from turtle import ht
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re 
from selenium import webdriver
import time
import pandas as pd
# Create an URL object
url = 'https://racerender.com/TrackAddict/docs/TrackList.html'
# Create object page
html_string = requests.get(url).content

soup = BeautifulSoup(html_string, 'html.parser')
table1 = soup.find_all("a", target="_trackmap")
tracks = []
browser = webdriver.Chrome("/Users/zabih/Documents/GitHub/enable-ninja-repo/code/src/server/chromedriver")
counter = 0
for a in table1:
    counter +=1
    track_name = re.findall('\>..*?\<',str(a))[0].strip('>').strip("<")
    link=a['href'].replace('&' , '&')
    link = link.replace('http://maps.google.com/maps' , 'https://www.google.com/maps')
    browser.get(link)
    browser.maximize_window()
    time.sleep(1)
    htmlstring = browser.find_element_by_class_name("x3AX1-LfntMc-header-title-VdSJob").text
    temp =htmlstring.split(',')
    tracks.append([track_name,temp[0],temp[1]])
    

with open('track_list.txt', 'w') as f:
    for item in tracks:
        f.write("%s\n" % item)


