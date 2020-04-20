

import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

class color:

   BOLD = '\033[1m'
   END = '\033[0m'

def get(url):
    driver=webdriver.Chrome(executable_path=r'[path to chrome driver]')

    driver.get(url)
    soup=BeautifulSoup(driver.page_source,'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    time.sleep(2)
    question_title_div = soup.find('div',class_='css-v3d350')
    time.sleep(2)
    question_title = question_title_div.get_text()
    time.sleep(2)
    question_statement_div=soup.find('div', class_='content__u3I1 question-content__JfgR')
    question_statement=question_statement_div.get_text()


    # ro = question_statement + ro
    # print('\033[1m' + question_statement)
    # print(ro)
    driver.quit()
    return question_title + "\n" + "\n" + question_statement


def getUrl(l,r,users_choice):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"[path to json file]", scope)
    client = gspread.authorize(creds)

    # users_choice='Easy Problems'

    if(users_choice=='medium'):
        sheet = client.open("NN_copy").worksheet('Medium Problems')
    elif(users_choice=='easy'):
        sheet = client.open("NN_copy").worksheet('Easy Problems')
    elif(users_choice=='hard'):
        sheet = client.open("NN_copy").worksheet('Hard Problems')

    # l=6
    # r=7
    list = []
    for i in range (l,r+1):
        cell=sheet.cell(i,5).value
        list.append(cell)

    return list


list=[]
url=[]
l=int(input())
r=int(input())
l=l+5
r=r+5
choice = input()
url = getUrl(l,r,choice)
# for a in url:
#     print(a)
# testing with multiple values for now
# url.append('https://leetcode.com/problems/move-zeroes/')
# url.append('https://leetcode.com/problems/sqrtx/')
# url.append('https://leetcode.com/problems/first-bad-version/')
# url.append('https://leetcode.com/problems/valid-perfect-square/')
# url.append('https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/')

for link in url:
    list.append(get(link) + "\n"+"\n")

changeline = '*'*200

name='output-'+choice+'-' + str(l) + '-' + str(r)+".txt"
f=open(r'[path to file]',"w+")
for str in list:
    f.write(str+"\n")
    f.write(changeline+"\n" + "\n")

f.close()
