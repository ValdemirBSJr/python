#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import re
import requests
import bs4
from requests.auth import HTTPBasicAuth
import telepot

'''
Nome do BOT: avisaIncidente
username do BOT: FOTEOTGbot
'''


bot = telepot.Bot('BOT-ID') #chave do bot

#print(bot.getMe())

print(bot.getUpdates())


print('Buscando página...')

enderecoFONTES = 'http://pagina-de-consulta/cgi-bin/status.cgi?host=all&servicestatustypes=28'

print('Página consultada..: ', enderecoFONTES)

consultaPagina = requests.get(enderecoFONTES, auth=HTTPBasicAuth('login', 'senha'))

print('Erro da consulta? ', consultaPagina.raise_for_status())

print('Fontes fora?')

# Página toda

# print(bs4.BeautifulSoup(consultaPagina.text, 'html.parser'))

lePagina = bs4.BeautifulSoup(consultaPagina.text, 'html.parser')

# fontesFora = lePagina.find_all('td', 'statusHOSTDOWN')

# fontesFora = lePagina.find_all(href=re.compile('extinfo.cgi?*'))


# print(fontesFora)


for tag in lePagina.find_all(href=re.compile('FONTE_')):

    print(tag.text)
    bot.sendMessage(-50764421, tag.text) #id do grupo NET
    bot.sendMessage(129300838, tag.text) # Meu ID
