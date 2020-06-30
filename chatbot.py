#!/home/valdemir/Documentos/PYTHON-PROJETOS/chatbot-wtz/venv/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

#https://medium.com/rafael-h-dias/chatbot-com-python-para-whatsapp-a8eaebbb33c5
#solução do erro de dependencia: https://github.com/gunthercox/chatterbot-corpus/issues/127

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from selenium import webdriver
import time
import os


class WppBot:
    def __init__(self):
        #quando vc nao instancia antes, nao recebe valor por parametro e todos os obj ficam com mesmo valor. Como nao vamos precisar de mais de um, tanto faz ter
        self.nome_contato = "Clau Tim"
        #Informamos onde esta noos chromedriver
        #configuracao PT-BR
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')

        self.driver = webdriver.Chrome(executable_path='./chromedriver')

        #variavel para o bot nao ficar respondendo a mesma mensagem sem parar. Uso mais a baixo
        self.ultimo_texto = ''

    def whatsapp(self):

        self.driver.get('https://web.whatsapp.com/')

        time.sleep(15)

        #entra na conversa ou grupo que escolhemos
        target = self.driver.find_element_by_xpath(f'//span[@title="{self.nome_contato}"]')

        time.sleep(3)

        target.click()


    def escuta(self):

        self.driver.get('https://web.whatsapp.com/')

        time.sleep(15)

        #metodo para escutar as mensagens recebidas no grupo
        #<span dir="auto" title="Central Antifa da Família" class="_3ko75 _5h6Y_ _3Whw5">Central Antifa da Família</span>
        #<div class="_2kHpK"><div class="_357i8"><div class="_3C
        #<span dir="ltr" class="_3Whw5 selectable-text invisible-space copyable-text"><span>Apois vou querer pra dar aula</span></span>

        post = self.driver.find_elements_by_class_name('_357i8')

        #print(str(post))

        #pegar o ultimo indice da conversa q vai ser salvo no post
        ultimo = len(post) - 1
        #print(ultimo)
        #vamos retornar o texto dessa ultima conversa

        texto = post[ultimo].find_elements_by_css_selector('span.selectable-text')

        self.texto = texto[len(texto)-1].text
        #self.texto = 'Teste'

        return self.texto


    def bot(self):
        #daremos um nome para o bot
        chatbot = ChatBot('Tob')
        #escolhemos a forma como o bot vai treinar
        trainer = ChatterBotCorpusTrainer(chatbot)
        #usaremos um corpus de dialogo para treina-lo
        trainer.train('chatterbot.corpus.portuguese.conversations')

        #agora um while para o bot ficar escutando
        while True:
            #O bot sempre estara chamando a funcao escuta
            texto = self.escuta()

            #Sempre transformar o retorno em string
            texto = str(texto)

            # "#>" é para o bot nao responder ele mesmo
            if texto != self.ultimo_texto and texto[0] != '#>':
                self.ultimo_texto = texto

                user_input = texto

                #Aqui o bot pegará a mensagem da pessoa e verá a melhor forma de
                #responder com base no que ele já sabe.
                self.bot_response = chatbot.get_response(user_input)

                #O processo a seguir é clicar na caixa de mensagem onde se digita o texto
                chatBox = self.driver.find_element_by_class_name("_3uMse")

                time.sleep(3)
                chatBox.click()

                #escrever na caixa com o #> no inicio
                chatBox.send_keys('#>' + str(self.bot_response))

                #Clicar no botao enviar
                botao_enviar = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
                time.sleep(3)
                botao_enviar.click()
                time.sleep(5)



if __name__ == '__main__':

    bot = WppBot()
    bot.whatsapp()
    time.sleep(30)
    bot.bot()
    #texto_impresso = WppBot()
    #texto_impresso.whatsapp()




