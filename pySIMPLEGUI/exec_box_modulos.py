#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra


import os
import pexpect as pxp
import shelve
import sys

class Ativa_dav:

    '''
    Slot aloca na memoria apenas espaço para as 2 variaveis.
    A classe recebe os attr de login e senha do arquivo shelve para logar
    '''

    __slots__ = ['_login', '_senha']

    def __init__(self, login='', senha=''):
        self._login = login
        self._senha = senha



if __name__ == '__main__':

    print('Tentando logar!...')
    try:

        #Crio o arquivo shelve e lhe imputo valores
        arquivoConf = shelve.open(os.path.join('db'))
        #login=''
        #senha=''
        #arquivoConf['login'] = login
        #arquivoConf['senha'] = senha
        #print('Login: {}. Senha: {}'.format(arquivoConf['login'], arquivoConf['senha']))



        input = Ativa_dav()
        input._login = arquivoConf['login']
        input._senha = arquivoConf['senha']

        comando = pxp.spawn('gio mount davs://dav.box.com')
        comando.expect('User: ')
        comando.sendline(input._login)
        comando.expect('Password: ')
        comando.sendline(input._senha)

        arquivoConf.close()

        print('Loguei, olha lá!!!')

    except Exception as erro:
        print('Não foi possível logar no Dav do BOX! Erro: ', erro)
        arquivoConf.close()
        sys.exit()




