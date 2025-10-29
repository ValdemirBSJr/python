#coding: utf-8

#author: Valdemir Bezerra

from kivy.app import App
from kivy.uix.button import Button

#Aqui criamos o evento pra quando o botão for precionado
def click():
    print("O botão for clicado")


def build():
    btn = Button()
    btn.text="Clique aqui"

    #Aqui fazemos a declaração do evento
    btn.on_press = click

    return btn

janela = App()
janela.build = build
janela.run()