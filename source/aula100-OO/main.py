#coding: utf-8
#Author: Valdemir

"""
Este código mostra a forma mais aconselhada para se trabalhar. Kivy orientado
a objeto Criamos uma classe chamada de meu programa e colocamos a função build dentro dela. Quando
for pra rodar o app chama a classe pra rodar. O codigo deve ser assim. Classe programa que extende App
"""

from kivy.app import App
from kivy.uix.label import Label

class MeuPrograma(App):

    def build(self):
        return Label()

MeuPrograma().run()