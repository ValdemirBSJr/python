#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import json

dadosJSON = '{"nome": "Sofia", "eGato?": true, "filhotes?": 0, "tipo": null}'

valorPython = json.loads(dadosJSON)

print(valorPython)

valorPadraoPython = {'eGato?': True, 'nome': 'Flufy', 'filhotes?': 2, 'tipo': 'Persa'}

valorParaJSON = json.dumps(valorPadraoPython)

print(valorParaJSON)