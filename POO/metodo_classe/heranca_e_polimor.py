#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import abc
#abc permite classe abstrata. Uma classe abstrata
#tem metodos e atributos para serem herdados, mas o objeto nao
#pode ser instanciado, apenas herdado.

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


class Gerente(Funcionario):
    '''
    Classe que herda de funcionario
    '''
    def __init__(self, nome, cpf, salario, senha, qrd_gerenciados):
        #Funcionario.__init__(nome, cpf, salario) #para que nao se sobrescreva
        super().__init__(nome, cpf, salario) #faz a mesma coisa da linha comentada acima. referencia a superclasse

        self._qrd_gerenciados = qrd_gerenciados
        self._senha = senha


    #def get_bonificacao(self):
        #return self._salario * 0.15 #Aqui sobrescrevemos o metodo para calcular valor diferente para o gerente

    def get_bonificacao(self):
        return super().get_bonificacao() + 1000 #Se quiser apenas acrescentar alguma funcionalidade a mais, pode fazer isso


    def autentica(self, senha):
        if self._senha == senha:
            print('Acesso permitido.')
            return True

        else:
            print('Acesso negado.')
            return False

class Diretor(Funcionario):
    def __init__(self, nome, cpf, salario):
        super().__init__(nome, cpf, salario)

    def get_bonificacao(self):
        return super().get_bonificacao() + 5000


class ControleDeBonificacoes:
    def __init__(self, total_bonificacoes=0):
        self._total_bonificacoes = total_bonificacoes


    #def registra(self, obj):
        #if(isinstance(obj, Funcionario)): #isinstance verifica o tipo da instância. Mas não é pythonico
            #self._total_bonificacoes += obj.get_bonificacao()
        #else:
            #print('Instância de {} não implementa o método get_bonificacao.'.format(self.__class__.__name__))

    #def registra(self, obj):
        #if(hasattr(obj, 'get_bonificacao')): #verifica se o objeto possui aquele atributo. Também não é considerado pythonico
            #self._total_bonificacoes += obj.get_bonificacao()
        #else:
            #print('Instância de {} não implementa o método get_bonificacao()'.format(self.__class__.__name__))

    def registra(self, obj):
        try:
            self._total_bonificacoes += obj.get_bonificacao() #o jeito pythonico é usar o try catch e deixar o erro estourar (0_o)
        except AttributeError as e:
            print(e)


    @property
    def total_bonificacoes(self):
        return self._total_bonificacoes



class Cliente:
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



#funcionario = Funcionario('João', '111111111-11', 2000.0)
#print(vars(funcionario)) #vars ve os atributos do objeto
#print('bonificação do funcionário: {}'.format(funcionario.get_bonificacao()))

gerente = Gerente('José', '222222222-22', 5000.0, '1234', 0)
#print(vars(gerente))
print('bonificação do gerente: {}'.format(gerente.get_bonificacao()))

controle = ControleDeBonificacoes()
#controle.registra(funcionario)
controle.registra(gerente)

print('Total: {}'.format(controle.total_bonificacoes))

cliente = Cliente('Maria', '000000-0', '321')

controle2 = ControleDeBonificacoes()
controle2.registra(cliente)

diretor = Diretor('joao', '111111111-11', 4000.0)
controle3 = ControleDeBonificacoes()
controle3.registra(diretor)
print('Total: {}'.format(controle3.total_bonificacoes))




