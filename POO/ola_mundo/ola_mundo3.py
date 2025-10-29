#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''

Aqui a forma mais simples de se criar uma classe e os
atributos do objeto

'''

class Conta():
    def __init__(self, numero, titular, saldo, limite):

        print('Inicializando uma conta')

        self.numero = numero
        self.titular =  titular
        self.saldo = saldo
        self.limite = limite

    def deposita(self, valor):
        self.saldo += valor

    def saca(self, valor):
        if self.saldo < valor:
            return False
        else:
            self.saldo -= valor
            return True

    def extrato(self):
        print(
            'O cliente: {} de conta: {}\nAcaba de depositar: {}\nSaldo em conta: {}'.format(conta.titular, conta.numero, conta.saldo, conta.limite))


conta = Conta('123-4', 'Jão', 120.0, 1000.0)
print(type(conta))

conta.extrato()

conta.deposita(20.0)

conta.extrato()

tentativaSaque = 3000.0

consegui = conta.saca(tentativaSaque)

if consegui:

    conta.extrato()
else:
    print('Não foi possível realizar o saque.\n O valor sacado é maior do que o em conta.\nValor em conta: {}.\nValor digitado: {}.'.format(conta.limite, tentativaSaque))


