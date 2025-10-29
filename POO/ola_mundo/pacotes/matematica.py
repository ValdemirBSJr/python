#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''

Para atrelar um modulo de outro projeto, vc tem que primeiro transformar ele em um pacote.
Para isso: clica no botão esquerdo do mouse > python package
Pode mover ou copiar o arquivo para o pacote(pasta)

'''

def soma(parcela, parcela_2):
    return parcela + parcela_2

if __name__ == '__main__':
    print(soma(1,1))