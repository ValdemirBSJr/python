#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra
# https://pt.stackoverflow.com/questions/186982/jeito-pythonico-de-definir-setters-e-getters

class Pessoa:

    __slots__ = ['_nome', '_idade']

    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade


    #Como encapsular os getters e setters
    '''
    Em python só se encapsula quando vc tem mais alguns comportamentos para atribuir aos atributos,
    como validar o bd e afins
    caso nao, só usar normal como acima. Caso precise, veja exemplo do nome abaixo
    '''

    @property
    def nome(self):
        # Este código é executado quando alguém for
        # ler o valor de self.nome
        return self._nome


    @nome.setter
    def nome(self, valor):
        # este código é executado sempre que alguém fizer self.nome = valor
        self._nome = valor





#classe que vai herdar de Pessoa
class Pessoa_fisica(Pessoa):

    __slots__ = ['_CPF']

    def __init__(self, CPF, nome, idade):

        #importa caracteristicas da classe pessoa
        super().__init__(nome, idade)
        self._CPF = CPF





p1 = Pessoa(nome='joão', idade=22)

print(p1._nome)

p1._idade = 34

print(p1._idade)


pf1 = Pessoa_fisica(nome='Zohan', idade=34, CPF='000.000.000.01')

print(f'Nome da PF: {pf1._nome}. Idade: {pf1._idade}. CPF: {pf1._CPF}')

pf1._idade = 35

print(pf1._idade)

