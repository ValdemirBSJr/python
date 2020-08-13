#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra


import os
import sys
from mandaEmail import MandaEmail



caminho = '/home/user/Documentos/SCRIPTS/erros_crontab/'
listaArquivos = []
conteudoArquivos = []


if os.path.exists(caminho):

    try:


        for arquivo in os.listdir(caminho):
            #print('O arquivo: ',arquivo,' tem o tamanho: ', os.path.getsize(os.path.join(caminho, arquivo)))
            if os.path.getsize(os.path.join(caminho, arquivo)) > 1:
                listaArquivos.append(arquivo)

                linhasArquivo = open(os.path.join(caminho, arquivo))
                linhasContidas = linhasArquivo.read()
                conteudoArquivos.append(linhasContidas)


        #print(listaArquivos)
        if not listaArquivos:
            print("Tudo OK, não temos problemas listados nos arquivos de log!!!")
        else:
            print('Oops! Encontramos um ou mais erros nos arquivos: ', listaArquivos, 'descritivo por email.')
            print('')
            print('Mandando email...:')




            #MandaEmail(nome=','.join(listaArquivos), descricao=','.join(conteudoArquivos))
            MandaEmail(nome=','.join(listaArquivos), descricao=','.join(conteudoArquivos))

            print('Enviado!!')

    except:
        print('Erro inexperado: ', sys.exc_info()[0])

else:
    print('O caminho: ', caminho, 'Não está acessível ou não existe.')





