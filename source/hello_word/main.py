#coding: utf-8

# importamos as bibliotecas
from kivy.app import App
from kivy.uix.label import Label

#Funcao que ira retornar os componentes
def build(): # Função que acrescenta os componentes
    return Label(text = "Hello World")

#App().run() roda a aplicação

#atribuir os elementos da blioteca para o hello world
hello_word = App() # associa a instancia do app ao aplicativo que queremos criar
hello_word.build = build
hello_word.run()