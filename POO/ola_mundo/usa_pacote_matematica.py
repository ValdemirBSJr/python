#!/home/datacenter/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''

Para atrelar um modulo de outro projeto, vc tem que primeiro transformar ele em um pacote.
Para isso: clica no botão esquerdo do mouse > python package
Pode mover ou copiar o arquivo para o pacote(pasta)

'''

#As duas formas abaixo funcionam:

#from pacotes.matematica import soma as so

#print(so(1,2))

import pacotes.matematica

print(pacotes.matematica.soma(1,4))