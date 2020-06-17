#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra


import os
import pexpect as pxp
import shelve
import PySimpleGUI as sg

class Tela_Log_Box:
    def __init__(self):

        sg.change_look_and_feel('DarkBrown4')

        #layou da app
        layout = [

            [sg.Text('Login: ',size=(6,0)), sg.Input(size=(30,0), key='login')],
            [sg.Text('Senha: ', size=(6,0)), sg.Input(size=(15,0),  password_char='*', key='senha')],
            [sg.Button('Conectar'), sg.Button('CANCELAR')],
            [sg.Output(size=(300,200), background_color='black', text_color='white')],
        ]

        #janela/form
        self.janela = sg.Window('Efetuar Login no BOX', grab_anywhere=True, size=(500,400)).layout(layout)

    def Iniciar(self):

        while True:

            self.event, self.values = self.janela.read()



            if self.event in (None, 'CANCELAR'):
                break
            if self.event in ('Conectar'):

                #verifica se os cammpos estao vazios. Se um dos dois estiver, nao faz nada
                if len(self.values['login']) == 0 or len(self.values['senha']) == 0:
                    sg.popup_ok('Os campos login e senha não podem estar vazios!', title='Erro')


                else:
                    login_digitado = self.values['login'].strip()
                    senha_digitada = self.values['senha'].strip()
                    #print(login_digitado)

                    #desabilita o botão até tudo estar terminado, visible para sumir com ele
                    self.janela['Conectar'].Update(disabled=True)

                    try:

                        arquivo_Conf = shelve.open(os.path.join('/home/valdemir/Documentos/PYTHON-PROJETOS/pySIMPLEGUI/db'))
                        verify_login = arquivo_Conf['login']
                        verify_senha = arquivo_Conf['senha']
                        arquivo_Conf.close()

                        if (login_digitado == verify_login) and (senha_digitada == verify_senha):
                            print('Olá! Começando o login...')

                            #magica do pexpect
                            print('Montando disco remoto em: gio mount davs://dav.box.com')
                            comando = pxp.spawn('gio mount davs://dav.box.com')
                            comando.expect('User: ')
                            comando.sendline(login_digitado)
                            print('Passando o login... Feito!')
                            comando.expect('Password: ')
                            comando.sendline(senha_digitada)
                            print('Passando a senha... Feito!')
                            print('BOX pronto para uso!')

                        else:
                            sg.popup_ok('Desculpe, mas login ou senha estão incorretos. Tente de novo', title='Erro ao logar')

                            #limpa os campos para nova tentativa
                            self.janela['login'].Update('')
                            self.janela['senha'].Update('')

                    except Exception as Erro:
                        sg.popup_scrolled(f'Não foi possível executar o login no dav!\nCódigo do erro: {Erro}')
                        arquivo_Conf.close()


                    #terminado tudo, habilita o botao
                    self.janela['Conectar'].Update(disabled=False)



        self.janela.close()


if __name__ == '__main__':
    telaApp = Tela_Log_Box()
    telaApp.Iniciar()

