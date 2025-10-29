#!/home/valdemir/e38/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

from selenium import webdriver
import time


class WhatsappBot:
    def __init__(self):
        self.mensagem = 'Bom dia pessoal, veja o video que acabou de sair https://www.youtube.com/watch?v=ISYHWfWvp3E&list=WL&index=39&t=0s'
        self.grupos = ['_357i8️💙']
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path='./chromedriver')

    def EnviarMensagens(self):
        #<span dir="auto" title="Central Antifa da Família" class="_3ko75 _5h6Y_ _3Whw5">Central Antifa da Família</span>
        #<div tabindex="-1" class="_3uMse"><div tabindex="-1" class="_2FVVk _2UL8j"><div class="_2FbwG" style="visibility: visible">Digite uma mensagem</div><div class="_3FRCZ
        #<span data-icon="send"
        #<div class="_357i8">
        #<span dir="auto" title="Central Antifa da Família" class="_3ko75 _5h6Y_ _3Whw5">Central Antifa da Família</span>


        self.driver.get('https://web.whatsapp.com/')
        time.sleep(15)

        for grupo in self.grupos:
            grupo = self.driver.find_element_by_css_selector('span._3ko75 _5h6Y_ _3Whw5')
            time.sleep(3)
            grupo.click()
            chat_box = self.driver.find_element_by_class_name("_3uMse")
            time.sleep(3)
            chat_box.click()
            chat_box.send_keys(self.mensagem)
            botao_enviar = self.driver.find_element_by_xpath("//span[@data-icon='send']")
            time.sleep(3)
            botao_enviar.click()
            time.sleep(5)

if __name__ == '__main__':
    bot = WhatsappBot()
    bot.EnviarMensagens()



