#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''
exemplo de list comprehension: Se quiser computar o quadrado de uma lista

expressões geradoras servem pra fazer a mesma coisa,
mas um passo na iteração de cada vez, para não dar stack overflow
'''

lista = [1,2,3,4,5,6]

quadrado = [x**2 for x in lista]
print(quadrado)

#se quiser o quadrado apenas dos numeros divisiveis por 2
so_pares = [x**2 for x in lista if x % 2==0]
print(so_pares)

#expressões geradoras:
raiz = ((x, x**0,5) for x in lista)

print(next(raiz))
print(next(raiz))