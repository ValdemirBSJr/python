#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#Script para consultar os MAC's do PEV usando bs4

from modulos import verificaCaminho
from modulos import lerLista
from modulos import fazConsulta

caminho = '/home/user/Documentos/SCRIPTS/consultaPEV/entrada/macs.txt'

if verificaCaminho(caminho) == 'valido':
    print('Trabalhando na lista, primeiro, vamos ler e formatar os MAC\'s...')
    listaMAcs = lerLista(lista=caminho)

    fazConsulta(listaMontada=listaMAcs)

    #print(listaMAcs)




else:
    print('Deu errado')



