#!python3
#coding: utf-8
#author: valdemir

# Para executar entre no k35 > na pasta e aplique o comando> # Para executar entre no k35 > na pasta e aplique o comando > C:\dev\kivy\excript\app-comerciais-kivy\aulas\curso-scrapy\aula31-comecandoScrapy> scrapy runspider inicio.py
import scrapy

# A unidade basica é o spider que vai na pagina buscar as informacoes
class GilenoSpider(scrapy.Spider):
    name = 'gilenofilho' #nomeia a spider

    start_urls = {'http://www.gilenofilho.com.br'} #cria a lista no qual vai fazer a busca

    #A funcao parse vai pegar os valores da lista start_urls para ir buscar os conteudos em cada
    def parse(self, response):
        self.log('Hello World')
        self.log(response.body) #Vai buscar o body da pagina da vez

# Para executar entre no k35 > na pasta e aplique o comando> # Para executar entre no k35 > na pasta e aplique o comando > C:\dev\kivy\excript\app-comerciais-kivy\aulas\curso-scrapy\aula31-comecandoScrapy> scrapy runspider inicio.py

