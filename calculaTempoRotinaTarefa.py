#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import time

def calculaProduto():
    #Calcula o produto dos 100.000 primeiros numeros
    produto = 1

    for i in range(1, 100000):
        produto *= i

    return produto

comecoMarcadorTempo = time.time()

prod = calculaProduto()

fimMarcadorTempo = time.time()

print('O resultado do produto: %s' %(len(str(prod))))

print('Levou %s segundos para calcular.' %str((fimMarcadorTempo - comecoMarcadorTempo)))