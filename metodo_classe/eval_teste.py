#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class Ponto:
    '''

    A função eval() recebe uma stringe
    tenta executar essa string como um comando do Python

    '''

    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __str__(self): #utilizado para apresentar mensagens para os usuários da classe, de maneira mais amigável
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self): #é usado para representar o objeto de maneira técnica
        return 'Ponto({}, {})'.format(self.x+1, self.y + 1)

if __name__ == '__main__':
    p1 = Ponto(1,2)
    p2 = eval(repr(p1))

    print(p1)
    print(p2)