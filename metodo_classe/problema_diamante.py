#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''
 O ptyhon resolve a ordem das classes de acordo com o MRO (Method resolution order)
 Abaixo, veremos a orde da classe diretor. Isso server para diminuir ambiguidade em relação as heranças
 quem herda o que.
 Para resolver esse problema, usar o super que sabe lidar com herança multipla
 '''

class A:
    def m1(self):
        print('método de A')

class B(A):
    def m1(self):
        super().m1()

    def m2(self):
        print('método de B')

class C(A):
    def m1(self):
        super().m1()
    def m2(self):
        print('método de C')
class D(B,C):
    def m1(self):
        super().m1()

    def m2(self):
        super().m2()

if __name__ == '__main__':
    d = D()
    d.m1()
    d.m2()
    print(D.mro())