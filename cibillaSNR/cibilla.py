#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import telebot
import logging
from moduloCibilla import return_font, return_node, return_ofensors, return_client
from telebot import util
import telegram
import time


#id of oraculoSNRbot
bot_id_token = 'IDO DO BOT'

#instance the bot
bot = telebot.TeleBot(bot_id_token)

@bot.message_handler(commands=['start', 'help', 'ajuda', 'inicio'])
def sendStartMessage(message):

    bot.reply_to(message, 'Olá, eu sou o Oráculo do SNR! \n Digite o node que quer consultar e tentarei trazer alguma informação para você.\nExemplo: \"/nodeJP35\" ou \"/node STNAA\".\nDigite \"/fonte\" e irei trazer o status da fonte e o endereço. Exemplo: \"/fonteJP117\".\nDigite \"/ofensores\" para retornar os piores nodes no momento.')


@bot.message_handler(commands=['criador'])
def sendCreator(message):

    bot.reply_to(message, 'Eu fui criado por Valdemir Bezerra de Souza Júnior para auxiliar a técnica.\n Email: ')


@bot.message_handler(content_types=['document', 'audio'])
def sendDocs(message):
    bot.reply_to(message, 'Olá! \nMeu criador me fez pra retornar nodes o status dos nodes e não pra trocar documentos.\n Por favor digita um node válido. Exemplo:\n EX1 ou EX2.')

@bot.message_handler(regexp=r'^/fonte*')
def handle_message(message):

    if message.chat.type == 'private':
        messageInt = 'Olá! Respondo apenas mensagens no grupo de SNR!'
        bot.reply_to(message, messageInt, parse_mode=telegram.ParseMode.HTML)
    else:
        messageInit = return_font(message.text)

        if messageInit == None:
            messageInit = 'Nada retornado!\nNão conseguimos achar uma fonte com estes parâmetros.\nPode ser que não tenhamos uma fonte cadastrada para este node.'

        if len(messageInit) > 4090:
            for x in range(0, len(messageInit), 4090):
                bot.reply_to(message, messageInit[x:x+4090], parse_mode=telegram.ParseMode.HTML)
                time.sleep(1)
        else:
            bot.reply_to(message, messageInit, parse_mode=telegram.ParseMode.HTML)



@bot.message_handler(regexp=r'^/node*')
def handle_message(message):

    #user_id = message.from_user.id
    #print(user_id)

    if message.chat.type == 'private':
        messageInt = 'Olá! Respondo apenas mensagens no grupo de SNR!'
        bot.reply_to(message, messageInt, parse_mode=telegram.ParseMode.HTML)
    else:

        messageInt = return_node(message.text)

        if messageInt == None:
            messageInt = 'Nada retornado!\nPode ser que o node esteja sem sinal total. Favor ligar para o SETOR.'

        #if  text is larger than 4090, split that

        if len(messageInt) > 4090:
            for x in range(0, len(messageInt), 4090):
                bot.reply_to(message, messageInt[x:x+4090], parse_mode=telegram.ParseMode.HTML)
                time.sleep(1)



        else:
            #end split text
            bot.reply_to(message, messageInt, parse_mode=telegram.ParseMode.HTML)



@bot.message_handler(regexp=r'^/ofensores')
def handle_message(message):

    messageInt = return_ofensors(message.text)

    if messageInt == None:
        messageInt = 'Nada retornado!\nNão temos ofensores no momento, ou estamos com problemas.'


    #if  text is larger than 4090, split that
    if len(messageInt) > 4090:
        for x in range(0, len(messageInt), 4090):
            bot.reply_to(message, messageInt[x:x+4090], parse_mode=telegram.ParseMode.HTML)
            time.sleep(1)

    else:
        #end split text
        bot.reply_to(message, messageInt, parse_mode=telegram.ParseMode.HTML)



@bot.message_handler(regexp=r'^/cli')
def handle_message(message):
    messageInt = return_client(message.text)

    if messageInt == None:
        messageInt = 'Nada retornado!\nCliente não pode ser localizado. retorno vazio.'
        bot.reply_to(message, messageInt, parse_mode=telegram.ParseMode.HTML)

    else:

        #split large text acordding the telebot lib example
        #split the text in 4090 characters
        splitted_text = util.split_string(messageInt, 4090)
        for text in splitted_text:
            bot.reply_to(message, text, parse_mode=telegram.ParseMode.HTML)



if __name__ == '__main__':

    #for loggin erros
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    '''
    this line start the microservice that has 
    to be constantly running to be able to respond
     and perform tasks via command. 
     If it stops spinning, it will stop responding
    '''
    bot.polling(none_stop=False)

