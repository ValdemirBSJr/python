#!/home/env python3
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import socket, sys

class Scan_Port:

    '''
    execute com:
    :param 1 -> ip ou
    :param 2 -> ip + porta ou
    :param 3 -> ip + porta inicial + porta final
    '''


    def escaneia(self) ->str:

        args = sys.argv


        if len(args) == 3:

            print()
            print('Escaneando portas, pode durar algum tempo...')

            try:

                for ports in range(1, 65535):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if s.connect_ex((sys.argv[2], ports)) == 0:
                        print('PORTA: ', ports, ' ABERTA')
                        s.close()

                print()
                print('Finalizado!')

            except Exception as erro:
                print(f'Oops, ocorreu o seguinte erro na consulta..: {erro}')

        elif len(args) == 4:

            print('')
            print('Verificando a porta...')

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if s.connect_ex((sys.argv[2], int(sys.argv[3]))) != 0:
                print('PORTA: ', sys.argv[3], ' FECHADA')
            else:
                print('PORTA: ', sys.argv[3], ' ABERTA')
                s.close()

        elif len(args) == 5:

            print()
            print(f'Verificando as portas no intervalo {sys.argv[3]}:{sys.argv[4]} do ip: {sys.argv[2]}')

            try:

                for ports in range(int(sys.argv[3]), int(sys.argv[4])):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    if s.connect_ex((sys.argv[2], ports)) == 0:
                        print('PORTA: ', ports, ' ABERTA')
                        s.close()

                print()
                print('FIM')

            except Exception as erro:
                print(f'Oops, ocorreu o seguinte erro na consulta de intervalo..: {erro}')

if __name__ == '__main__':

    print('Vamos verificar algumas portas?')
    print('Digite apenas o ip para uma varredura completa,')
    print('Digite ip e porta ou intervalo de portas separados por espaço para intervalo.')
    print()
    print()
    escaneia = Scan_Port()
    escaneia.escaneia()
