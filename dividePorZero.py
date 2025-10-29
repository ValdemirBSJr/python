#Author: Valdemir Bezerra
# encoding: utf-8

"""
Esse script simula erro de divisao por zero.
Mas o erro sera tratado com try/except (mesma coisa do try/catch

"""
import random


def divide(dividePor):
    try:
        return 42 / dividePor
    except:
        print("Erro: nao pode dividir um numero por zero")


print(divide(0))


for i in range(6):
    print(divide(random.randint(1,6)))

