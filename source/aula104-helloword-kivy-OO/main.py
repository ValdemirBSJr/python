#coding: utf-8
#Author: Valdemir

# quando o kivy roda, ele vai buscar um arquivo com o mesmo nome e em letra minuscula. No caso criamos o arquivo
# hello.kv e ele puxa altomaticamente

from kivy.app import App
from kivy.uix.label import Label

class HelloApp(App):

    pass
    #def build(self):
     #   return Label(text="Hello World")


HelloApp().run()