#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

class complexo():

    '''

    primeiro exemplo.
    Vamos criar uma classe para representar numeros complexos.

    no metodo __init__, representamos o valor do real e imaginario do numero complexo

    '''

    def __init__(self, real, imag):
        self._real = real
        self._imag = imag



c = complexo(1,0)

print(c._real)
print(c._imag)


class complexo_comple():

    """
    Abaixo construo quatro metodos para a tratativa do n complexo
    e 2 propriedades
    """

    def getReal(self):
        return self._real

    def setReal(self, valor):
        self._real = valor

    real = property(

        fget=getReal,
        fset = setReal
    )

    def getImag(self):
        return  self._imag

    def setImag(self, valor):
        self._imag = valor

    imag = property(

        fget=getImag,
        fset=setImag
    )

d = complexo_comple()
d.imag = 2
d.real = 3
print(d.real)
print(d.imag)

d.setImag(4)

print(d.imag)