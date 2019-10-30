#Aqui vamos ver como importar e de onde importar os modulos python (bibliotecas, dll, so etc)
#O python tem pastas padrão pra colocar la, mas voce pode alterar o local facilmente

#abaixo uma importacao de função para mostrar os path ou caminhos

from pprint import pprint
from sys import path as lpath # aqui dou um alias pois path tem um nome muito comum

import sys #para poder incluir uma pasta como sourcepath

pprint(lpath)

#sys.path.insert(0, "C:\\dev\\kivy\\excript\\app-comerciais-kivy\\aulas\\Modulos e Pacotes") #Aqui incluimos o caminho da nova pasta no sourcepath de forma explicita. Tem que estar toda a vez. Como o path é tratado como lista, o zero serve pra dizer que vai em primeiro lugar
#para colocar permanentemente, clique com o botao direito em cima > Ultima opcao 'Mark directory as sourceCode'

print("Aí o caminho do sistema")

pprint(sys.path)

import ferramenta


# Resultado:

#['C:\\dev\\kivy\\excript\\app-comerciais-kivy\\aulas',
#  'C:\\dev\\kivy\\excript\\app-comerciais-kivy',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\python36.zip',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\DLLs',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\lib',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\lib\\site-packages',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\lib\\site-packages\\win32',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\lib\\site-packages\\win32\\lib',
#  'C:\\Users\\seyro\\Anaconda3\\envs\\k35\\lib\\site-packages\\Pythonwin']

