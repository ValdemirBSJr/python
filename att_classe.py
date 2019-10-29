#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra


class Conta:

    '''

    Aqui verificamos como criamos uma variavel de classe.
    Ela pode ter valor unico para cada chamada e não é acessada igualmente por todos os objetos
    ùtil quando se quer acessar um valor para 2 objetos de mesmo tipo instanciados simultaneamente
    '''

    #total_contas = 0 #Global
    _total_contas = 0 #Agora ele ta protegido
    def __init__(self, saldo):
        self._saldo = saldo
        Conta._total_contas += 1

    @staticmethod #esse decoretor é para nao precisar passar o self
    def get_total_contas():
        return Conta._total_contas


c1 = Conta(100.0)
print(c1.get_total_contas())
c2 = Conta(200.0)
print(c2.get_total_contas())

#podemos acessar a variavel diretamente
print(Conta._total_contas)

#Abaixo se torna possível pois esta como metodo estatico, caso nao esteja tem que passar o valor
#print(Conta.get_total_contas(c1))
print(Conta.get_total_contas())


