#!/home/valdemir/Documentos/PYTHON-PROJETOS/chatbot-wtz/venv/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra
#https://chatterbot.readthedocs.io/en/stable/examples.html

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

#instanciamos um bot e damos nome a ele
chat_bot = ChatBot('Bill')

#selecionamos a forma como o bot vai treinar
trainer = ChatterBotCorpusTrainer(chat_bot)

#BD com a conversacao
trainer.train('chatterbot.corpus.portuguese.conversations')

print('Digite algo para começar a conversar com seu bot..:')

while True:
    try:
        bot_input = chat_bot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit) as Erro:
        print(f'Erro no bot. Erro: {Erro}')




