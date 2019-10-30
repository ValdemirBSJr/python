#coding: utf-8

#Author: Valdemir Bezerra

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout # layout vai conter todos os elementos de tela
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.core.window import Window #Pacote pra redimensionar a janela

def click():
    print(txt.text + " Adicionado")


def build():
    layout = FloatLayout()

    global txt #Aqui eu declarei a variavel como global pra poder chama-la na funcao click NÃO RECOMENDADO
    txt = TextInput(text="Valdemir")
    txt.size_hint = None, None
    txt.height = 300
    txt.width = 400
    txt.y = 200 #distancia do topo
    txt.x = 100 #distancia da margem esquerda

    btn = Button(text="Clique aqui")
    btn.size_hint = None, None
    btn.width = 200
    btn.height = 50
    btn.y = 140
    btn.x = 200

    #Abaixo acoplamos os elementos no widget
    layout.add_widget(txt)
    layout.add_widget(btn)

    btn.on_press = click

    return layout
    #pass # diz que a função será implementada posteriormente

janela = App()
janela.title = "Aula 99"

Window.size = 600, 600

janela.build = build
janela.run()