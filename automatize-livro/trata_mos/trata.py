#Author: Valdemir Bezerra
#coding: utf-8
#for: NET


#Imports

from datetime import date
import requests
import bs4



print('''
  _______                  _               __  __    ____     _____  
 |__   __|                | |             |  \/  |  / __ \   / ____| 
    | |     _ __    __ _  | |_    __ _    | \  / | | |  | | | (___   
    | |    | '__|  / _` | | __|  / _` |   | |\/| | | |  | |  \___ \  
    | |    | |    | (_| | | |_  | (_| |   | |  | | | |__| |  ____) | 
    |_|    |_|     \__,_|  \__|  \__,_|   |_|  |_|  \____/  |_____/ 
            
                        powered on PYTHON!!!
                        developer: N5669203
''')

#Aqui tenho um dicionario com os meses do ano para buscar a pagina do MOS pela data do dia anterior

mes = {0:'lixo', 1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
endereco_MOS = ['http://vqr.virtua.com.br/get_vqr_status.php?data=', '10-OCT-17', '&switch_id=114&switch_name=JPADTCDPI-01&schema_version=v766']

hoje = date.today()
diaTratativa = date.fromordinal(hoje.toordinal()- 1)
anoTratativa = str(diaTratativa.year)

#print(str(diaTratativa.day) + '-' + str(mes[diaTratativa.month]) + '-' + anoTratativa[2:4])


#Aqui eu monto a string para buscar a pagina

#Abaixo temos o endereco ja pronto para fazer a consulta, mas para testes vou usar o endereço local
#consultaMOS = endereco_MOS[0] + str(diaTratativa.day) + '-' + str(mes[diaTratativa.month]) + '-' + anoTratativa[2:4] + endereco_MOS[2]

#Aqui seto o endereco local. para usar a web usar o request
paginaMOS = open('html_teste\VQR - Call Scores.html')

paginaSoup = bs4.BeautifulSoup(paginaMOS.read(), "html.parser") #caso de erro no linux, tirar a referencia ao html5lib

elementoHTML = paginaSoup.select('td > a')

print(len(elementoHTML)) #mostra quantos retornos temos. eh criado uma lista

#print(elementoHTML[2].getText()) # tras o texto

#print(elementoHTML[2]) #tras o elemento

#print(elementoHTML[2].attrs) # pega os atributos. com isso pego o link, conforme abaixo

#pegaLinkPagina = elementoHTML[2].attrs

#print(pegaLinkPagina['href'])

contador = 0
for link in range(2, len(elementoHTML)): #Forma muito mais elegante e que tras o resultado correto, abaixo tem outra forma comentada
    print(elementoHTML[link].get('href'))
    contador +=1 #só pra ver quanto retornou

print(contador)



#recebeLinks = [] #Pra receber os links listados

#for link in paginaSoup.find_all('a', string='Detail'): #Aqui faço um for que pega apenas os links que contenha a string 'Detail' pra pegar só os links validos pra tratar o MOS. Pula os 'nao disponivel'
#    print(link['href']) #retorna so o link
 #   recebeLinks = link['href']

#print(len(recebeLinks))

################################### Aqui vamos pegar os valores da pagina do resultado do MOS







