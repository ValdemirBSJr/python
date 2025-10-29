#coding: utf-8
#Author: Valdemir Bezerra

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

def funcSelf(x):
    print("funcSelf")

Button.funcSelf = funcSelf #acessao endereco de memoria e associa ele ao botao

class MinhaTela(BoxLayout):
    def funcRoot(self):
        print("funcRoot")





class Estudo5App(App):
    #pass #indica que nao ha implementacao da classe
    def funcApp(self):
        print("funcApp")

janela = Estudo5App()
janela.run()