#!python3
# -*- coding: utf-8 -*-
#author: valdemir

import requests

jogos = requests.get('http://worldcup.sfg.io/matches').json()

for jogo in jogos:
    if jogo['status'] in ('completed', 'in progress'):
        print(jogo['home_team']['country'], jogo['home_team']['goals'], jogo['home_team']['code'], 'x', jogo['away_team']['country'], jogo['away_team']['goals'])