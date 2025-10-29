#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg

usuario = ''

#Funcao para criar as janelas
def janela_login():

    sg.theme('Reddit')
    layout = [

        [sg.Text('Nome')],
        [sg.Input(key='usuario')],
        [sg.Button('Continuar')],
    ]


    #sem esse finalize ele nao abre a janela
    return sg.Window('Login', layout=layout, finalize=True)

def janela_pedido(usuario):

    sg.theme('Reddit')

    layout = [

        [sg.Text(f'Fazer pedido para {usuario}')],
        [sg.Checkbox('Pizza Peperoni', key='pizza1'), sg.Checkbox('Pizza Frango c/ Catupiry', key='pizza2')],
        [sg.Button('Voltar'), sg.Button('Fazer pedido')],
    ]
    return sg.Window('Montar pedido', layout=layout, finalize=True)

#criamos as 2 janelas mas só chamamos a primeira, para a segunda só aparecer quando for chamada
#são criadas quando abre o programa, pode criar depois
janela1, janela2 = janela_login(), None


while True:
    #loop para ficar as janelas sendo exibidas, sem esse loop, ao clicar no botao ele encerra
    #escuta as janelas eventos e valores de todas as janelas instanciadas
    window, event, values = sg.read_all_windows()

    if window == janela1 and event == sg.WIN_CLOSED:
        #quando a janela for fechada
        break
    if window == janela2 and event == sg.WIN_CLOSED:
        break
    if window == janela1 and event == 'Continuar':
        usuario = values['usuario']
        janela2 = janela_pedido(usuario)
        janela1.hide()
    if window == janela2 and event == 'Voltar':
        janela2.hide()
        janela1.un_hide()
    if window == janela2 and event == 'Fazer pedido':
        if values['pizza1'] == True and values['pizza2'] == True:
            sg.Popup('Foram solicitadas pizzas de peperoni e frango')
        elif values['pizza1'] == True and values['pizza2'] == False:
            sg.Popup('Foi solicitada uma pizza de peperoni')
        elif values['pizza1'] == False and values['pizza2'] == True:
            sg.Popup('Foi solicitada uma pizza de frango')
