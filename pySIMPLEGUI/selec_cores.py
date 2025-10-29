#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg

choices = ('Vermelho', 'Verde', 'Azul', 'Amarelo', 'Laranja', 'Roxo', 'Salmão')

layout = [  [sg.Text('Qual sua cor favorita?')],
            [sg.Listbox(choices, size=(15, len(choices)), key='-COLOR-', enable_events=True)] ]

window = sg.Window('Selecione uma cor', layout)

while True:                  # loop evento
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values['-COLOR-']:    # se alguma cor for selecionada na lista
        sg.popup(f"Sua cor favorita é {values['-COLOR-'][0]}")
window.close()