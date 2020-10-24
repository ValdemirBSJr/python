# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import schedule
import time

def fazer_tarefa_importante():
    print('Fazendo a tarefa')

#schedule.cada.tempo.fazer
#A cada 10 segundos fazer a chamada a função
#da pra por dias horas minutos anos ou ate nos dias da semana>>> every().monday.do()
#every().monday.at('08:00')
#every().day.at('08:00')
schedule.every(10).seconds.do(fazer_tarefa_importante)

if __name__ == '__main__':
    while 1:
        schedule.run_pending()
        time.sleep(1) #so pra dar tempo de executar o print, nao precisa em script grande

