#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class Teste():
    def __init__(self, nome):
        self.nome = nome

    def retornaNome(self, retNome):
        self.nome = retNome

        if self.nome =='':
            print('String Vazia')
        else:
            for i, v in enumerate(self.nome):
                print('Índice {} | Letra {}'.format(i, v))


variavel = Teste('Valdemir')
print(variavel.nome)

variavel.retornaNome(variavel.nome)