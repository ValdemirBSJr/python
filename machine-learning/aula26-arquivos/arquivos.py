#!python3
#coding: utf-8
#author: valdemir

arquivo = open('arquivo.txt', 'a')

arquivo.write('machine learning\n')

arquivo.flush()

arquivo.close()

### ABAIXO forma mais resumida de acessar

texto ="""

    Aprendendo machine Learning e datacience
    Python é muito legal!!!
"""
with open('arquivo.txt', 'a') as f:
    f.write(texto)

with open('arquivo.txt', 'r') as f:
    for linha in f.readlines():
        print(linha)

    #Pode ser assim tambem pra ler tudo:
        # conteudo = f.read()
        #print(conteudo)

#forma de buscar um elemento:
# with open('arquivo.txt', 'r') as f:
#   lista = f.read().splitlines()
#print(lista[0])