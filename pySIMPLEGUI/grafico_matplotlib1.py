# !/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import PySimpleGUI as sg
import matplotlib.pyplot as plt

"""
Janela PySimpleGUI simultânea e uma janela interativa Matplotlib. 
Várias pessoas solicitaram a capacidade de executar uma janela PySimpleGUI 
normal que inicia uma janela MatplotLib que é interativa com os controles comuns do Matplotlib. 
Acontece que é uma coisa bastante simples de fazer. O segredo é adicionar parâmetro block=False to plt.show()
"""

def draw_plot():
    plt.plot([0.1, 0.2, 0.5, 0.7])
    plt.show(block=False)

layout = [[sg.Button('Plotar'), sg.Cancel(), sg.Button('Popup')]]

window = sg.Window('gerando um gráfico Matplotlib....', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'Plotar':
        draw_plot()
    elif event == 'Popup':
        sg.popup('Sim, o app ainda está rodando...')
window.close()
