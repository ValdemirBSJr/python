#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import re


busca1 = '''🤖 Detectei uma oportunidade!

Jogo: :soccer: SCR Altach v Mattersburg
Aposta: BACK Over 2.5 Goals FT
Odd: @1.40'''

busca2 = '''🤖 Detectei uma oportunidade!

Jogo: :soccer: Leicester v Brighton
Campeonato: English Premier League
Aposta: BACK Over 0.5 Goals HT
Odd: @1.48'''

criterioBusca = re.findall(r'Jogo: :.*|Aposta:.*', busca2)


print(criterioBusca)

jogo = criterioBusca[0].split(':')
aposta = criterioBusca[1].split(' ')

jogo = jogo[3].replace(' v ', ' x ')
jogo = jogo.replace('SCR', '')

print(jogo)
print(aposta[3],aposta[5])