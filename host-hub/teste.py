#!/home/valdemir/e38/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

#https://easysnmp.readthedocs.io/en/latest/

from easysnmp import Session

#Cria uma sessao SNMP para sewr usada por todos os requests
sessao = Session(hostname='localhost', community='public', version=1)

#pesquisando uma informacao com o get
localizacao = sessao.get('.1.3.6.1.2.1.1.1.0')

print(localizacao)