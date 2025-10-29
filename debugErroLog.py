#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#Podemos salvar os erros em arquivo de log
# importamos o modulo traceback para poder coletar os erros

import traceback
from datetime import date

hoje = date.today()

try:
    raise Exception('Esta eh uma mensagem de erro')

except:
    errorFile = open('errorInfo.txt', 'w')
    errorFile.write('Erro ocorreu em: ' + str(hoje.strftime("%H:%M:%S - %d/%m/%Y")) + "\n\n")
    errorFile.write(traceback.format_exc())
    errorFile.write(("-" * 80) + "\n\n")
    errorFile.close()

    print("A mensagem de erro foi salva em errorInfo.txt")

