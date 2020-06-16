#!/home/valdemir/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg
import time

#texto = sg.popup_get_file('Selecione um arquivo')
#sg.popup_scrolled('Arquivo selecionado', 'Arquivo que você selecionou', texto, yes_no=True)
#data = sg.popup_get_date()
#sg.popup('Data selecionada', 'Data que voce selecionou..:', data)

sg.popup_animated(image_source='/home/valdemir/Documentos/PYTHON-PROJETOS/pySIMPLEGUI/gifee2.gif', message='carregando...', grab_anywhere=True, keep_on_top=True, alpha_channel=0.9)
time.sleep(3)
sg.popup_animated(image_source=None) #fecha todos os popup animados

for i in range(1,1000):
    sg.one_line_progress_meter('Meu medidor', i+1, 1000, 'Chave','Mensagem opcional', orientation='h',)

#se quiser depurar algo facil em uma janela use o PRINT:

for i in range(100):
    sg.Print(i)