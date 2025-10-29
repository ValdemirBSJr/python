#Author: Valdemir Bezerra
# encoding: utf-8


import random, sys

for i in range(5):
    print(random.randint(1, 10))


while True:
    print("Digite sair para sair.")
    resposta = input()

    if resposta == "sair":
        sys.exit()

    print("Voce digitou '" + resposta)
