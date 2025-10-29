#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra


import PySimpleGUI as sg

sg.theme('DarkBrown1')

layout = [  [sg.Text('Cronômetro', size=(20, 2), justification='center')],
            [sg.Text(size=(10, 2), font=('Helvetica', 20), justification='center', key='-OUTPUT-')],
            [sg.T(' ' * 5), sg.Button('Start/Stop', focus=True), sg.Quit()]]

window = sg.Window('Contador do Cronômetro', layout)

timer_running, counter = True, 0

while True:                                 # Loop de evento
    event, values = window.read(timeout=10) # Tente usar o mais alto valor de tempo limite possível
    if event in (sg.WIN_CLOSED, 'Quit'):             # fecha o app se clicar no x ou no botão sair
        break
    elif event == 'Start/Stop':
        timer_running = not timer_running
    if timer_running:
        window['-OUTPUT-'].update('{:02d}:{:02d}.{:02d}'.format((counter // 100) // 60, (counter // 100) % 60, counter % 100))
        counter += 1
window.close()