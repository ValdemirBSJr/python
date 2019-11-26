#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#pra iterar sobre conjunto de inteiros, usar o range
for i in range(4):
    print(i)

#para uma estrutura de dados, iterar diretamente
lista_sabores = ['baunilha', 'chocolate', 'morango']
for sabor in lista_sabores:
    print(f'{sabor} é delicioso!')

#enumerate é a função nativa para iterar por estruturas
#de dados e pegar seu indice. Pode usar até o numero de inicio da contagem
#se nao especificar começa do zero
for i, sabor in enumerate(lista_sabores, 1):
    print(f'Índice:{i} sabor: {sabor}')

#############################################

#Para iterar em 2 ou mais listas em paralelo, usar zip
#zip usa tuplas contendo os valores da iteração
#zip só funciona bem se as listas tiverem o mesmo tamanho
#se as listas forem diferentes, usar zip_longest da lib itertools

nomes = ['Luiz', 'Pedro', 'Eduardo']
contador_letras = [len(n) for n in nomes]


nome_mais_longo = None
max_letras = 0

for nome, contagem in zip(nomes, contador_letras):
    if contagem > max_letras:
        nome_mais_longo = nome
        max_letras = contagem

print(nome_mais_longo)


