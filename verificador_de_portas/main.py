#!/home/env python3
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

'''
PAra executar rode no terminal e passo o ip como parâmetro
'''

import socket, sys

def verifica_Portas() -> str:

    args = sys.argv

    #print(args)



    if len(args) == 2:


        try:

            for ports in range(1, 65535):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if s.connect_ex((sys.argv[1], ports)) == 0:
                    print('PORTA: ', ports, ' ABERTA')
                    s.close()

        except Exception as erro:
            print(f'Oops, ocorreu o seguinte erro na consulta..: {erro}')

    elif len(args) == 3:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if s.connect_ex((sys.argv[1], int(sys.argv[2]))) != 0:
            print('PORTA: ', sys.argv[2], ' FECHADA')
        else:
            print('PORTA: ', sys.argv[2], ' ABERTA')
            s.close()

    elif len(args) == 4:
        try:

            for ports in range(int(sys.argv[2]), int(sys.argv[3])):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if s.connect_ex((sys.argv[1], ports)) == 0:
                    print('PORTA: ', ports, ' ABERTA')
                    s.close()

        except Exception as erro:
            print(f'Oops, ocorreu o seguinte erro na consulta..: {erro}')




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('Vamos verificar algumas portas?')
    print('Digite apenas o ip para uma varredura completa,')
    print('Digite ip e porta ou intervalo de portas separados por espaço para intervalo.')
    print()
    print()

    verifica_Portas()
