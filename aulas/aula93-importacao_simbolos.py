# se nao quiser copiar a biblioteca toda, podemos copiar apenas alguns simbolos (elementos isolados)

#aqui eu posso importar o modulo e criar um alias:

# import math as matematica

# from math import e as euler, pi as numero_pi

# pra importar todos os simbolos de um módulos (Não recomendado):
# from modulo import *

from math import pi, e
from math import sqrt #aqui eu importo a funcao de raiz quadrada, mas é o mesmo procedimento

def funcaoFatorial():
    from math import factorial
    print(factorial(10))

print(pi)
print(e)
print(sqrt(9))
funcaoFatorial()