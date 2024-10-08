#!/home/env python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import telebot
import os
import re
from datetime import datetime

#Karlbetbot


botId = 'ID_DO_BOT' #meubotSNR

bot = telebot.TeleBot(botId)


def retorna_parte_link(link_completo):



    criterio_busca = re.findall(r'Jogo: .*|Aposta:.*', link_completo)



    if criterio_busca == None:
        return f'Oops! Aconteceu algum erro!\nNão consegui retornar as apostas no texto encaminhado!\nEu só trabalho com mensagens encaminhadas com os textos do betfair!'

    else:

        jogo = criterio_busca[0].split(':')
        aposta = criterio_busca[1].split(' ')



        jogo = jogo[1].replace(' v ', ' x ')
        jogo = jogo.replace('\u26bd', '') #mata o emoji \u26bd
        jogo = jogo.lstrip()
        jogo = jogo.replace('SCR', '')


        texto_para_salvar = ' '


        if aposta[5] == 'FT':
            texto_para_salvar = jogo + ' / Mais/Menos de ' + aposta[3]

        if aposta[5] == 'HT':
            texto_para_salvar = jogo + ' / Golos na 1.ª parte ' + aposta[3]


        agora = datetime.now()

        estado_arquivo = 'a'

        f = open(os.path.join('/home/caminho_bot', 'dados.txt'), 'r')
        qtde_linhas = f.readlines()



        if len(qtde_linhas) > 9:
            estado_arquivo = 'w'




        with open(os.path.join('/home/caminho_bot', 'dados.txt'), estado_arquivo) as arquivo:
            arquivo.write(f'{texto_para_salvar}\n')
            arquivo.close()

        return f' Salvo no BD: {texto_para_salvar} em: {agora.strftime("%d/%m/%Y %H:%M")}'


#========================================================================================

@bot.message_handler(commands=['start', 'help', 'ajuda', 'inicio'])
def send_welcome(message):
    bot.reply_to(message, "Olá, eu sou o BetBot do Karl!\nMinha função é salvar em um arquivo todos os índices do link?")

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    message_pronta = retorna_parte_link(message.text)
#    bot.reply_to(message, message_pronta)

@bot.message_handler(regexp=r'^.*Detectei uma oportunidade!*')
def handle_message(message):
    message_pronta = retorna_parte_link(message.text)
    bot.reply_to(message, message_pronta)

@bot.message_handler(regexp=r'^(?!.*Detectei uma oportunidade!/*)')
def handle_message(message):
    message.text = 'Olá, só trabalho com oportunidades do betfair!'
    bot.reply_to(message, message.text)




if __name__ == '__main__':
    print('Ouvindo...')
    bot.polling()
    print('parado!')
