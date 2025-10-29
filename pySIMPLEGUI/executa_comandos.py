#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg
import subprocess



def ExecuteCommandSubprocess(command, *args):
    try:
        sp = subprocess.Popen([command, *args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sp.communicate()
        if out:
            print(out.decode("utf-8"))
        if err:
            print(err.decode("utf-8"))
    except:
        pass


layout = [
    [sg.Text('Saída do script...:', size=(40, 1))],
    [sg.Output(size=(88, 20))],
    [sg.Button('script1'), sg.Button('script2'), sg.Button('SAIR')],
    [sg.Text('Comando Manual', size=(15, 1)), sg.InputText(focus=True), sg.Button('Rodar', bind_return_key=True)]
]

window = sg.Window('Script launcher', layout)



while True:
    (event, value) = window.read()
    if event == 'SAIR' or event == sg.WIN_CLOSED:
        break  # exit button clicked
    if event == 'script1':
        ExecuteCommandSubprocess('pip', 'list')
    elif event == 'script2':
        ExecuteCommandSubprocess('pwd')
    elif event == 'Rodar':
        ExecuteCommandSubprocess(value[0])