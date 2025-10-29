#!python3
#coding: utf-8
#author: valdemir

import requests
from bs4 import BeautifulSoup

resposta = requests.get('http://www.gilenofilho.com.br/')

print(str(resposta.status_code)) #resposta 200 = OK

soup = BeautifulSoup(resposta.text, 'html.parser')

print(soup.find('title')) # primeira tag de titulo title

link = soup.find('h3', attrs={'class':'ctitle'}) # pega o primeiro

print(link)

links = soup.find_all('h3', attrs={'class':'ctitle'}) # pega todos

for l in links:
    print(l)

