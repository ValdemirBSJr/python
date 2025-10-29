#coding: utf-8

# importamos as bibliotecas
from kivy.app import App
from kivy.uix.label import Label

#Funcao que ira retornar os componentes

def build():

    lb = Label()
    lb.text="Curso de python e Kivy"
    lb.italic=True
    lb.font_size=50
    return lb

    #return Label(text = "Curso de python e Kivy", italic=True, font_size=50)

#App().run() roda a aplicação

#atribuir os elementos da blioteca para o hello world

app = App()
app.build = build

app.run()


