#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

def exibe_kwargs(**kwargs):
    print(kwargs['valor1'])
    print(kwargs['valor2'])
    print(type(kwargs['valor3']))

    for i in kwargs['valor4']:
        print(i)

exibe_kwargs(valor1="Ola", valor2="kwarguis", valor3=0, valor4=['0', '1', '2'])

testeSplit = "JPADTCRTD01.sh"
retornoRoteador = testeSplit.split(".")
print(retornoRoteador[0])