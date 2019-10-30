#!python3
#coding: utf-8
#author: valdemir

import sys, os, pyperclip

SENHAS = {'email':'senhaemail',
          'blog': 'senhablog',
          'banco': 'senhabanco'}

"""
Quando se passa argumentos pro programa, o primeiro é o nome dele que 
vai automatico. A partir disso, pode passar outros parametros.
A condicao abaixo ve se foi passado algum parametro, se nao foi ele avisa
"""

if len(sys.argv) < 2:
    print("Uso: python senhas.py [conta] - copiado senha da conta")
    sys.exit()


conta = sys.argv[1] # O primeiro argumento é o nome da conta

if conta in SENHAS:
    pyperclip.copy(SENHAS[conta])
    print("Senha da conta de %s foi copiado para o clipboard" % conta)
    print(pyperclip.paste())
else:
    print("Não há uma conta com esse nome: %s" % conta)


os.system("Pause")