#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import subprocess
import PySimpleGUI as sg

CHROME = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


layout = [  [sg.Text('Text area', key='_TEXT_')],
            [sg.Input(key='_URL_')],
            [sg.Button('Chrome'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
  event, values = window.read()
  print(event, values)
  if event == sg.WIN_CLOSED or event == 'Exit':
    break
  if event == 'Chrome':
        sp = subprocess.Popen([CHROME, values['_URL_']], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

window.close()