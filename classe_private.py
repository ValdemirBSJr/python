#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class privada():
    def __init__(self, valorPrivado, valorPublico):

        '''
        Em python para colocar um valor privado que só pode ser trabalhado dentro da classe,
        não usamos o atributo private como em C# e sim dois underscore antes do nome. Fazendo isso ele
        só pode ser acessado dentro da classe. Se não por, ele será acessado do nosso código todo.

        :param valorPrivado: só acessível de dentro da classe
        :param valorPublico: acessível de todo o código
        '''

        self.__valorPrivado = valorPrivado
        self.valorPublico = valorPublico

        print('Valor privado: {}'.format(self.__valorPrivado)) #Aqui ele nao dá erro


retorna_valor_privado_sem_erro = privada('Valor privado', 'valor público')
#Abaixo ele vai dar erro por que tá chamando valor privado de fora da classe
#print('Valor privado: {} | Valor público: {}'.format(retorna_valor_privado_sem_erro.__valorPrivado, retorna_valor_privado_sem_erro.valorPublico))


retorna_valor_privado_sem_erro.__privada__idade = 20
print(retorna_valor_privado_sem_erro.__privada__idade) #Aqui criamos um atributo dinamicamente

#print(help(privada))