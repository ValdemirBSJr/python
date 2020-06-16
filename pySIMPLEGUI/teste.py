#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import PySimpleGUI as sg

class TelaPython:
    def __init__(self):

        sg.change_look_and_feel('Dark Blue 3')
        #para construir uma app 3 partes:

        #layout(arranjo dos componentes por linhas e dentro dessas linhas tem os componentes)
        layout = [
            [sg.Text('Nome', size=(5,0)), sg.Input(size=(15,0), key='nome')],
            [sg.Text('Idade', size=(5,0)), sg.Input(size=(15,0), key='idade')],
            [sg.Text('Quais emails você possui?')],
            [sg.Checkbox('Gmail', key='gmail'),sg.Checkbox('Outlook', key='outlook'), sg.Checkbox('Yahoo', key='yahoo')],
            [sg.Text('Aceita cartão?')],
            [sg.Radio('Sim', 'cartoes', key='aceita_cartao'), sg.Radio('Não', 'cartoes', key='nao_aceita_cartao')],
            [sg.Slider(range=(0,100), default_value=0, orientation='h', size=(15,20), key='slider_velocidade')],
            [sg.Button('Enviar Dados')],
            [sg.Output(size=(30,20))]
        ]

        #janela
        self.janela = sg.Window('Dados do Usuário', grab_anywhere=True).layout(layout) #grab=voce pode arrastar a janela

        #Extrair dados da tela. Sem o while abaixo, pode ser aqui
        #self.button, self.values = self.janela.Read()

    def Iniciar(self):

        while True: #sem o while a janela fecha depois do clique no botão

            #Extrair dados da tela
            self.event, self.values = self.janela.Read()

            #print(self.values) #aqui mostra todos os valores capturados
            nome = self.values['nome']
            idade = self.values['idade']
            aceita_gmail = self.values['gmail']
            aceita_outlook = self.values['outlook']
            aceita_yahoo = self.values['yahoo']
            aceita_cartao_sim = self.values['aceita_cartao']
            nao_aceita_cartao = self.values['nao_aceita_cartao']
            velocidade = self.values['slider_velocidade']

            print(f'Nome: {nome}. Idade: {idade}')
            print(f'Aceita GMAIL? {aceita_gmail}')
            print(f'Aceita Outlook? {aceita_outlook}')
            print(f'Aceita YAHOO? {aceita_yahoo}')
            print(f'Aceita cartão? {aceita_cartao_sim}')
            print(f'Não aceita cartão? {nao_aceita_cartao}')
            print(f'Velocidade: {velocidade}')






if __name__ == '__main__':
    tela = TelaPython()
    tela.Iniciar()

