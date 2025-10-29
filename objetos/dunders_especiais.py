#!/home/valdemir/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

class num:
    "Classe que simula um numero inteiro"
    pass
print(help(num))

####################################

class numeroint:
    def __init__(self, numero):
        self.numero = numero

    def __repr__(self):
        return 'Numero: {}'.format(self.numero) #classe pra representar o numero

    def __add__(self, op):
        return self.numero + op #classe para somar numero a obj

    def __radd__(self, op):
        return self.numero + op #classe reversa para somar independente da ordem


    def __mul__(self, op):
        return self.numero * op #classe para multiplicar
    def __rmul__(self, op):
        return  self.numero * op

n = numeroint(7)

print(n)

print('n + 2= ', n+2)
print('2 + n= ', 2+n)
print('2 * n= ', n*2)

############################################################

class Fila:
    def __init__(self, *args):
        self.f = list(args)

    def __repr__(self):
        return f'Fila: {self.f}'

    def __setitem__(self, instance, value): #se nao usar esses dunders daqui pra baixo, a lista não fica iteravel
        self.f[instance] = value

    def __getitem__(self, posicao):
        return self.f[posicao]

    def __lshift__(self, val): #acrescenta um elemento
        self.f.append(val)

    def __rshift__(self, val): #retira um elemento
        self.f.remove(val) if val < len(self.f) else 'feijoada'

    def __len__(self): #para retornar o len
        return len(self.f)


print(Fila(2,2,2,2,2).f)
print(Fila(3,3,3,3,3))

filaa = Fila(1,2,3,4)
filaa[2] = 7
filaa << 10 # para acrescentar mais um (lshift)

print(filaa[2])

for x in filaa:
    print(x)

filaa >> 1

print(filaa)

filaa << 13

print(filaa)
##########################
# Classe chamada como funcao

class func:
    def __init__(self, val):
        self.val = val
    def __call__(self):
        print(self.val)

f = func(1000)
f()

##################################3
class c:
    """
    documentaocao da classe
    """
    pass

print(c.__doc__)