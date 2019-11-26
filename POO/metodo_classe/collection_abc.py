#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''
Para criar um objeto do tipo dict que só aceita um objeto
como entrada aceitável. Isso serve para limitar a entrada
de informações em uma determinada lista apenas de algo que se
queira, para evitar lixo ou informações erradas que possam
quebrar o codigo. Aí usamos o collections.ABC para podermos
garantir que só um determinado objeto pode ser inputado e iterado.
Quem faz isso é o modulo container.
Modulo sized para retornar o tamanho do container
Modulo Iterable torna o container mutavel
MutableSequence torna o container iteravel e pega a posicao
'''

import csv
from collections.abc import Container, Sized, Iterable, MutableSequence
import abc

class Funcionarios(MutableSequence):
    _dados = []

    def __contains__(self, posicao):
        #metodo para sobrescrever/guardar a posicao
        return self._dados.__contains__(self, posicao)

    def __len__(self):
        #junto com o sized, retorna o tamanho do container
        return len(self._dados)

    def __iter__(self):
        #junto com o modulo Iterable este metodo deixa o container iteravel
        return self._dados.__iter__()

    def __getitem__(self, posicao):
        #pega o item
        return self._dados[posicao]

    def __setitem__(self, chave, valor):
        #seta o item. pra ver se o objeto setado é uma instancia de funcionario, usa o isinstance. Se nao for da erro
        if (isinstance(valor, Funcionarios)):
            self._dados[chave] = valor
        else:
            raise ValueError('valor atribuído não é um funcionário.')

    def __delitem__(self, chave):
        #deleta um item
        del self._dados[chave]

    def insert(self, chave, valor):
        #mesma coida do setitem
        if(isinstance(valor, Funcionarios)):
            return self._dados.insert(chave, valor)
        else:
            raise ValueError('Valor atribuído não é um funcionário.')



try:
    arquivo = open('funcionarios.txt', 'r')
    leitor = csv.reader(arquivo)

except Exception as e:
    print('Erro ao abrir o txt. Erro({})'.format(e))


    funcionarios = Funcionarios()

if __name__ == '__main__':


    for linha in leitor:
        funcionario = Funcionarios(linha[0], linha[1], linha[2])
        funcionarios.append(funcionario)

    arquivo.close()

    print('SALÁRIO - BONIFICAÇÃO')

    for f in funcionarios:
        print('{}'.format(f.salario))
