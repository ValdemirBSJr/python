#!/home/env python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import telebot
import os
import re
from datetime import datetime

#Karlbetbot

botId = 'BOT_ID'

bot = telebot.TeleBot(botId)

def retorna_parte_link(link_completo) -> str:

    retornar_so_link = re.compile(r'https://www.betfair.com/.*')

    busca = retornar_so_link.search(link_completo)


    if busca == None:
        return f'Oops! Aconteceu algum erro!\nNão consegui retornar o link no texto encaminhado!\nEu só trabalho com mensagens encaminhadas com o links do betfair!'

    else:

        link_completo = busca.group()
        parte_importante = link_completo.split('/')
        parte_importante = parte_importante[-1].split('.')


        agora = datetime.now()

        with open(os.path.join('/home/sua_pasta/bot-Telegram-Karl', 'dados.txt'), 'a') as arquivo:
            arquivo.write(f'{parte_importante[-1]}\n')
            arquivo.close()

        return f' Salvo no BD: {parte_importante[-1]} em: {agora.strftime("%d/%m/%Y %H:%M")}'


#========================================================================================

@bot.message_handler(commands=['start', 'help', 'ajuda', 'inicio'])
def send_welcome(message):
    bot.reply_to(message, "Olá, eu sou o BetBot do Karl!\nMinha função é salvar em um arquivo todos os índices do link?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    message_pronta = retorna_parte_link(message.text)
    bot.reply_to(message, message_pronta)

#@bot.message_handler(regexp=r'^https://www.betfair.com/*')
#def handle_message(message):
#    message_pronta = retorna_parte_link(message.text)
#    bot.reply_to(message, message_pronta)

#@bot.message_handler(regexp=r'^[https://www.betfair.com/*]')
#def handle_message(message):
#    message.text = 'Olá, só trabalho com links do betfair!\nLinks como esse: https://www.betfair.com...'
#    bot.reply_to(message, message.text)




if __name__ == '__main__':
    print('Ouvindo...')
    bot.polling()
    print('parado!')
