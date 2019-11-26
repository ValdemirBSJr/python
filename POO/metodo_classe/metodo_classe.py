#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class Conta:
    '''

    Métodos estáticos não devem ser confundidos com métodos de classe.
    Como os métodos estáticos, métodos de classe não são ligados às instâncias, mas sim a classe.
    O primeiro parâmetro de um método de classe é uma referência para a classe, isto é,
    um objeto do tipo class que por convenção nomeamos como 'cls'.
    Eles podem ser chamados via instância ou pela classe e utilizam um outro decorar, o @classmethod
    '''

    _total_contas = 0
    def __init__(self):
        type(self)._total_contas += 1

    @classmethod
    def get_total_contas(cls):
        return cls._total_contas

c1 = Conta()
print(c1.get_total_contas())
c2 = Conta()
print(c2.get_total_contas())

print(Conta.get_total_contas())