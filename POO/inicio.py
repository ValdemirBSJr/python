#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

'''
Cria uma classe animal
'''

class Animal:

    #slot serve para alocar um espaço definido em memoria, economiza memoria
    __slots__ = ['_tipo', '_nome', '_sexo', '_idade']

    def __init__(self, tipo=None, nome=None, sexo=None, idade=0):

        self._tipo = tipo
        self._nome = nome
        self._sexo = sexo
        self._idade = idade

    def comer(self):
        print(f'O animal {self._nome} do tipo: {self._tipo}, está comendo! Idade: {self._idade}. Sexo: {self._sexo}.')


bode = Animal(tipo='Mamífero', nome='Brabante', sexo='Masculino')
bode._idade = 10

bode.comer()

print(type(bode))

def soma(number1, number2) -> int:
    return print(number1 + number2)

soma(2,1)

