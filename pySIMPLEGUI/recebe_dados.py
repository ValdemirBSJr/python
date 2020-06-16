#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg

class Recebe_Dados:
    def __init__(self):
        sg.theme('DarkTeal')

        layout = [
            [sg.Text('Olá, aqui é a linha 1')],
            [sg.Text('Digite algo: '), sg.Input(size=(10,0), key='digitado')],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]

        self.janela = sg.Window('Receber dados', layout)

    def Iniciar_app(self):
        while True:
            self.event, self.values = self.janela.read()

            valor_digitado = self.values['digitado']

            if self.event in (None, 'Cancelar'): #se clicar em fechar janela ou botão cancelar encerra
                break
            if self.event in ('OK'): #se clicar no botão ok, executa o codigo
                print(f'Valor digitado: {valor_digitado}')
                sg.popup('Valor digitado', 'Segue texto digitado..: ', valor_digitado)


        self.janela.close()

if __name__ == '__main__':
    telaApp = Recebe_Dados()
    telaApp.Iniciar_app()

