#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra


from collections import UserDict, defaultdict, Counter, deque, namedtuple

class Pins(UserDict):

    '''
    Usando collections vc pode criar um objeto que funciona como
    um dicionario mas que pode ter características proprias.
    Por exemplo, abaixo eu crio um objeto que funciona como uma lista
    mas que só aceita chaves de tipo string. Se forma um objeto com
    características que eu quero. Se tentar passar algo, vira string e se nao der para
    virar, da erro. Perceba que ao imprimir todas as chaves sao string
    '''

    def __contains__(self, key):
        return str(key) in self.keys()

    def __setitem__(self, key, value):
        self.data[str(key)] = value



if __name__ == '__main__':
    pins = Pins(one=1)
    print(pins)
    pins[3] = 1
    lista = [1,2,3]
    #pins(lista) = 2 #da erro
    print(pins)

    '''
    defaultdict não é necessário verificar se uma chave está presente
    ou não
    '''
    cores = [('1', 'azul'),('2', 'amarelo'),('3','vermelho'),('1', 'branco'),('3', 'verde')]
    cores_favoritas = defaultdict(list)

    for chave, valor in cores:
        cores_favoritas[chave].append(valor)

    print(cores_favoritas) #Nao vai acusar key error

    #Counter é um contador que retorna a quantidade de ocorrencias de um item em uma estrutura de dados
    cores_lista = ['amarelo', 'azul', 'azul', 'vermelho', 'azul', 'verde', 'vermelho']
    contador = Counter(cores_lista)
    print(contador)

    #Deque é uma fila que da pra adicionar e remover elementos de ambos os lados
    fila = deque()
    fila.append('1')
    fila.append('2')
    fila.append('3')
    print(len(fila))
    fila.pop() #exclui elemento da direito
    fila.append('3') #adiciona elemento na direita
    fila.popleft() #exclui elemento da esquerda
    fila.appendleft('1') #adiciona elemento na esquerda
    print(fila)

    #namedtuple é uma tupla que tem uma chave/índice, mas nao pode ser alterada igual as tuplas
    Conta = namedtuple('Conta', 'numero titular saldo limite')
    conta = Conta('123-4', 'João', 1000.0, 1000.0)
    print(conta)
    print(conta.titular)