#coding: utf-8
#Author: Valdemir

nomeGatos = ['Mimi', 'Jurema', 'Princesa Caroline']

while True:
    print("Digite o nome do gato de número " + str(len(nomeGatos) + 1) + ". Ou digite enter para sair")
    nome = input()

    if nome == "":
        break

    nomeGatos = nomeGatos + [nome]

print("Os gatos atualmente na lista são:")

for nome in nomeGatos:
    print(nome)

