#!/home/env python3
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import sys, socket
from threading import *

def main():

    args = sys.argv
    if len(args) < 2:
        print('[!]Faltam argumentos para o programa! Finalizando...')
        sys.exit(1)

    ip = args[1]
    portas = args[2] if len(args) >= 3 else '1:65536'
    portas = (x for x in range(int(portas.split(':')[0]), int(portas.split(':')[1]) + 1))

    scan(ip, portas)

def banner(sckt, ip, porta):

    try:
        sckt.settimeout(1)
        sckt.connect((ip, porta))
        banner = sckt.recv(1024).decode().strip()
        assert banner
        return banner
    except:
        return 'Desconhecido'

def child(ip, port):

    try:

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.settimeout(0.3)
        if s.connect_ex((ip, port)) == 0:
            print(f'{port}/tcp open', end='|')
            print(banner(s, ip, port))

    except:
        pass

def scan(ip, portas):

    for c in portas:
        t = Thread(target=child, args=(ip, c))
        t.start()

if __name__ == '__main__':
    main()












