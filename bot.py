#!/home/env python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import telebot
import os
from datetime import datetime

#Karlbetbot

botId = 'ID DO BOT'

bot = telebot.TeleBot(botId)

def retorna_parte_link(link_completo) -> str:
    link_pra_salvar = link_completo
    parte_importante = link_completo.split('/')

    agora = datetime.now()

    with open(os.path.join('/home/valdemir/Documentos/PYTHON-PROJETOS/bot-Telegram-Karl', 'dados.txt'), 'a') as arquivo:
        arquivo.write(f'{agora.strftime("%d/%m/%Y %H:%M")}; Link: {link_pra_salvar};Informação: {parte_importante[-1]}.\n')
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

#@bot.message_handler(regexp=r'^/https://www.betfair.com/*')
#def handle_message(message):
#    messageInit = retorna_parte_link(message.text)
#    bot.reply_to(message, messageInit)




if __name__ == '__main__':
    bot.polling()