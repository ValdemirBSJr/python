#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''
Vamos tentar abrir um arquivo que não existe
mandatario tentar abrir ele antes, pois caso de erro(ele não existe)
não será tratado no finally
'''

def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Inputs inválidos!') from e

x,y = 6,2

try:
    resultado = divide(x,y)
except ValueError:
    print('Inputs invalidos meu!')
else:
    print(f'Resultado é {resultado}')


