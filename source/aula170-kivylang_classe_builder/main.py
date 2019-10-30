#coding: utf-8
#Author: Valdemir Bezerra

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder

code = """

BoxLayout:
    Button:
        text: "1"
    Button:
        text: "2"

"""

class Estudo6App(App):
    #pass #indica que nao ha implementacao da classe
    def build(self):
        return Builder.load_string(code)
        #pra colocar o codigo kivy junto ao arquivo python podemos tambem invocar via arquivo. load_file


janela = Estudo6App()
janela.run()