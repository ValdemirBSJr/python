#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class Conta:

    '''
    Para evitar que usuarios atribuam a uma classe um atributo dinamicamente sem nossa permissão,
    podemos utilizar uma variável embutida no Python chamada __slots__ que pode guardar uma lista
    de atributos da classe definidos por nós. O slot deve ser utilizado por que foi criado para economizar
    memoria pois aloca espaço apenas para os atributos que estão estipulados la

    '''

    __slots__ = ['_numero', '_titular', '_saldo', '_limite']

    def __init__(self, numero=0, titular='uno', saldo=0, limite=0.0):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._limite = limite

conta = Conta()

conta.nome = 'Conta'