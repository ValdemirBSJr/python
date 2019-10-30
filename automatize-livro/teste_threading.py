#!python3
#coding: utf-8
#Author: Valdemir

import threading, time

print("Começo do programa")

def tireUmCoxilo():
    time.sleep(5)
    print("Acorde!")


threadOBJETO = threading.Thread(target=tireUmCoxilo)
threadOBJETO.start()

print("Fim do programa!")