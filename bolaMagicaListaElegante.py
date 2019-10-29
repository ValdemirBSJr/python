#code: utf-8
#Author: Valdemir Bezerra

import random

mensagens = ['Isto eh certo', 'Sim, definitivamente', 'Tente novamente',
             'Tente novamente mais tarde', 'Concentre-se e tente novamente',
             'Minha resposta eh nao', 'Olhando de fora nao parece bom',
             'sem duvida']

tamanho = len(mensagens)

tamanho -= 1

escolha = mensagens[random.randint(0, tamanho)]

print(escolha)