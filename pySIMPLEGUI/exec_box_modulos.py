#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg
import os
import subprocess as sub
import pexpect

class Ativa_dav:

    __slots__ = ['_login', '_senha']

    def __init__(self, login='meulogin', senha='minhasenha'):
        self._login = login
        self._senha = senha


if __name__ == '__main__':

    input = Ativa_dav()

    comando = pexpect.spawn('gio mount davs://dav.box.com')
    comando.expect('User: ')
    comando.sendline(input._login)
    comando.expect('Password: ')
    comando.sendline(input._senha)


