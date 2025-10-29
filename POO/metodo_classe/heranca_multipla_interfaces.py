#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import abc

class Funcionario(abc.ABC):
    '''
    Classe funcionarios
    Salva os dados do mesmo

    '''

    def __init__(self, nome, cpf, salario):

        self._salario = salario
        self._cpf = cpf
        self._nome = nome
    @abc.abstractmethod
    def get_bonificacao(self):
        return self._salario * 0.10



class Autenticavel():


    def autentica(self, senha):

        pass

class Gerente(Funcionario, Autenticavel):
    '''
    Classe que herda de funcionario
    '''
    def __init__(self, nome, cpf, salario, senha, qrd_gerenciados=0):
        #Funcionario.__init__(nome, cpf, salario) #para que nao se sobrescreva
        super().__init__(nome, cpf, salario) #faz a mesma coisa da linha comentada acima. referencia a superclasse

        self._qrd_gerenciados = qrd_gerenciados
        self._senha = senha


    #def get_bonificacao(self):
        #return self._salario * 0.15 #Aqui sobrescrevemos o metodo para calcular valor diferente para o gerente

    def get_bonificacao(self):
        return super().get_bonificacao() + 1000 #Se quiser apenas acrescentar alguma funcionalidade a mais, pode fazer isso


    #def autentica(self, senha):
        #if self._senha == senha:
            #print('Acesso permitido.')
            #return True

        #else:
            #print('Acesso negado.')
            #return False

class Diretor(Funcionario, Autenticavel):
    def __init__(self, nome, cpf, salario, senha):
        super().__init__(nome, cpf, salario)
        self._senha = senha

    def get_bonificacao(self):
        return super().get_bonificacao() + 5000

class Cliente(Autenticavel):
    '''
    Essa classe nao extende de nenhuma.
    Vamos tentar forçar ele a pegar um metodo que ele nao tem.
    vai dar erro. A forma mais eficiente é usar o metodo hasattr
    que verifica se esse objeto tem esse metodo.
    '''

    def __init__(self, nome, cpf, senha):
        self._senha = senha
        self._cpf = cpf
        self._nome = nome


class Sistema_Interno:
    '''
    Essa classe ira fazer a validacao de se o objeto
    tem o metodo autentica como herança. se ele tiver, loga no sistema
    '''
    def login(self, obj):
        if (hasattr(obj, 'autentica')):
            obj.autentica
            print('{} é autenticável.'.format(self.__class__.__name__))
            return True
        else:
            print('{} não é autenticável.'.format(self.__class__.__name__))
            return False


if __name__ == '__main__':
    #Se tirar a herança da classe cliente ele acusa erro.
    diretor = Diretor('João', '111111111', 3000.0, '1234')
    gerente = Gerente('José', '222222222', 5000.0, '1235')
    cliente = Cliente('Maria', '33333333', '122')

    sistema = Sistema_Interno()
    sistema.login(diretor)
    sistema.login(gerente)
    sistema.login(cliente)

    '''
    O ptyhon resolve a ordem das classes de acordo com o MRO (Method resolution order)
    Abaixo, veremos a orde da classe diretor. Isso server para diminuir ambiguidade em relação as heranças
    quem herda o que
    '''
    print(Diretor.mro())

