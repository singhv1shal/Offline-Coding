from django.shortcuts import render
from .forms import InputForm

import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from selenium.webdriver.chrome.options import Options
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

class color:

   BOLD = '\033[1m'
   END = '\033[0m'
# Create your views here.
def home(request):
    form=InputForm()
    return render(request,'home.html',{'form':form})

def get(url):

    options=Options()
    options.add_argument("--headless")
    driver=webdriver.Chrome(executable_path=r'chromedriver',options=options)

    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'lxml')
    for script in soup(["script", "style"]):
        script.decompose()
    time.sleep(2)
    question_title_div = soup.find('div',class_='css-v3d350')
    time.sleep(1)
    question_title = question_title_div.get_text()
    time.sleep(1)
    question_statement_div=soup.find('div', class_='content__u3I1 question-content__JfgR')
    question_statement=question_statement_div.get_text()


    # ro = question_statement + ro
    # print('\033[1m' + question_statement)
    # print(ro)
    driver.quit()
    return question_title + "\n" + "\n" + question_statement


def getUrl(l,r,users_choice):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"NNhack-446c445bcf65.json", scope)
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

def scrapLeetCode(l,r,choice):
    list=[]
    url=[]
    l=l+5
    r=r+5
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
    f=open(name,"w+")
    for st in list:
        f.write(st+"\n")
    f.close()


def download(request):
    # print("-------------------hello")
    if request.method=='POST':
        # print("world")
        form=InputForm(request.POST)
        if form.is_valid():
            # print("hi   ")
            l=int(form.cleaned_data['start'])
            r=int(form.cleaned_data['end'])
            choice=form.cleaned_data['difficulty']
            print(l)
            print(r)
            print(choice)
            try:
                scrapLeetCode(l,r,choice)
            except Exception as e:
                print(e)
                # return HttpResponse('Sorry! Slow Internet Speed')
                return HttpResponse(e)
    return redirect('ProblemStatements:home')
