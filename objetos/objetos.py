#!/home/valdemir/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

class Esposa:
    tetas = 2

    def muer():
        print('ô mulé braba!')

print(Esposa.tetas)

Esposa.muer()

##############################

class Passaro:
    estado = 'indefinido'

    #as propriedades, o que o passaro pode fazer que os definem como tal
    def voar(self): #self indica que a funcao sempre vai referir a ela mesma. A quem esta recebendo a definicao
        self.estado = 'Voando'
        print(self.estado)

    def pousar(self):
        self.estado = "Parado"
        print(self.estado)


print(Passaro.estado)
#print(Passaro.voar()#Vai dar erro, puq voce não tem como passar o argumento do self

#Aqui informo a classe que os p1 e p2 pertencem a essa classe 'passaro'
p1 = Passaro()
p2 = Passaro()

#Aqui instancio ou seja exemplifico qual o estado dos dois passaros

p1.voar()
p2.pousar()

#agora que eles estão com os métodos, podemos ver o estado

print(p1.estado)
print(p2.estado)

#####################################3

class Fila:

    def __init__(self): #Esse método serve para instanciar uma fila para cada chamada. Se não tiver essa classe, todos os objetos criados ficaram na mesma fila
        self.fila = []

    def entrar(self, nome):
        self.fila.append(nome)

    def sair(self):
        self.fila.pop(0) # tira sempre quem entrar primeira


supermercado = Fila() #indico primeiro puq tenho que falar que é pra mim proprio: 'self'

supermercado.entrar('Eduardo')

supermercado.entrar('Luiz')

supermercado.entrar('Antonio')

print(supermercado.fila)#mostra quantos tem na fila

supermercado.sair()

print(supermercado.fila)