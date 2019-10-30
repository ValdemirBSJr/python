#coding: utf-8
#author: Valdemir Jr.


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

class RootWidget(FloatLayout): #Classe vai conter gerenciador de layout
    pass

class MedidaApp(App): # classe do app

    def build(self):
        return RootWidget()


MedidaApp().run()