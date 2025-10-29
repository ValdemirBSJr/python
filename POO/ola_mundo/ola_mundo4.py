#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''

Duas classes. Uma recebe o objeto da outra como atributo

'''

class Cliente():
    def __init__(self, nome, sobrenome, cpf):

        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf

class Conta():
    def __init__(self, numero, cliente, saldo, limite=1000.0):

        self.numero = numero
        self.titular = cliente
        self.saldo = saldo
        self.limite = limite



cliente = Cliente('Jão', 'Du lixo', '0001')
conta = Conta('123-4', cliente, 120.0)

print(conta.titular.nome)



