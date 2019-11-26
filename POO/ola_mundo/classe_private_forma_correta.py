#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra


class Conta():
    '''
    Para proteger os atributos de forma correta e pythonica,
    usamos os decorators abaixo quando for necessário getter e setter.

    Se projetamos uma classe com atributos publicos e sem metodos, quebramos as regras da classe.
    Por isso temos que ter atributos privados para getter e setter. Aí usamos decorators do python.
    Um desses decorators é o properties.
    O decorator do setter é sempre o nome da funcao seguido de .setter
    '''

    def __init__(self, saldo=0.0):
        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo):
        if (saldo < 0):
            print('saldo não pode ser negativo')
        else:
            self._saldo = saldo
            print('Saldo: {}'.format(self.saldo))


conta = Conta(1000.0)
conta.saldo = -300.0
