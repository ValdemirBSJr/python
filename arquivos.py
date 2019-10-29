#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import pprint

# Lindo arquivos
helloFile = open('hello.txt')

helloContent = helloFile.read()

print(helloContent)

linhasFile = open('arquivoLinhas')

print(linhasFile.readlines())

gatos = [{'nome': 'Sofie', 'descricao': 'gordo'}, {'nome': 'Flufy', 'descricao': 'persa'}]

fileObj = open('meusgatos.py', 'w')
fileObj.write('gatos = ' + pprint.pformat(gatos) + '\n')

fileObj.close()

import meusgatos

print(meusgatos.gatos)

print(meusgatos.gatos[0])
