#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg

minhaFonte = 'Ariel 32'
layout = [
    [sg.Text('Botão Clicado..: '), sg.Text('Nada ainda...', key='feedback')],
    [sg.Button('CIMA', size=(32,3), font=minhaFonte, button_color=('white','green'))],
    [sg.Button('ESQUERDA', size=(15,3), font=minhaFonte), sg.Button('DIREITA', size=(15,3), font=minhaFonte)],
    [sg.Button('BAIXO', size=(32,3), font=minhaFonte, button_color=('white', 'red'))],
    [sg.Button('SAIR')]
]

janela = sg.Window('Botões', layout)

while True:
    event, values = janela.read()
    janela['feedback'].Update(event) # mostra o texto do botão na label feedback
    print(event, values)

    if event in (None, 'SAIR'):
        break

janela.close()