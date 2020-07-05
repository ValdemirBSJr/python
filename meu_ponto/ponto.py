#!/home/valdemir/Documentos/PYTHON-PROJETOS/meu_ponto/venv/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra


import PySimpleGUI as sg
from datetime import date, datetime, timedelta
import time
import re
import modulo_ponto
import os
import shutil



class Tela_ponto:


    def __init__(self):

        sg.theme('random') #randomiza o tema

        #abaixo, converto uma data em string e mando para Text 'data'
        #o text 'data' é atualizado dinamicamente pelos atributos target e format do text 'data_personalizada'
        #hora atual e minuto atual sao jogadas nos campos data e hora final
        data_atual = date.today().strftime('%d/%m/%Y')
        hora_atual = datetime.now().hour
        minuto_atual = datetime.now().minute

        popular_list_box = modulo_ponto.Acesso_BD()
        lista_populada = popular_list_box.popula_lista()
        #print(lista_populada)

        #layout da aplicacao
        layout = [
            [sg.Text('Dia da marcação..:'), sg.Text(data_atual, key='data'), sg.CalendarButton('Usar outra Data?', target='data', key='data_personalizada', format='%d/%m/%Y'), sg.Checkbox('Madrugada?', change_submits=True, enable_events=True, default='0',key='madrugada')],
            [sg.Text('Horário de entrada'), sg.Input(key='-TIMEIN1-', size=(4,1), change_submits=True, do_not_clear=True, focus=True), sg.Text(':', pad=(0,0)),sg.Input(key='-TIMEIN2-', size=(4,1), change_submits=True, do_not_clear=True),  sg.Text('Horário de Saída'),sg.Input(hora_atual, key='-TIMEOUT1-', size=(4, 1), change_submits=True, do_not_clear=True), sg.Text(':', pad=(0, 0)),sg.Input(minuto_atual, key='-TIMEOUT2-', size=(4, 1), change_submits=True, do_not_clear=True)],
            [sg.Button('Salvar')],
            [sg.Text('Horários Salvos..:')],
            [sg.Listbox(values=lista_populada, size=(90,15), auto_size_text=True, key='-BOX-')],
            [sg.Button('Editar'), sg.Button('Excluir'), sg.Button('Exportar'), sg.Button('Sair')],
            [sg.Text()],
            [sg.Text()],
            [sg.Text('Author: Valdemir Bezerra', font=('Helvetica', 10, 'underline italic'))]

        ]

        #monto a janela
        self.janela = sg.Window('Controle dos horários', size=(700, 400)).layout(layout)





    def Iniciar(self):

        #Aqui inicializamos o loop que vai ficar escutando os eventos e valores
        while True:
            self.event, self.values = self.janela.read()

            if self.event in (sg.WIN_CLOSED, 'Sair'): #Se clicar em fechar ou X, finalizamos a janela e o app
                self.janela.close()
                break

            if self.event == 'Salvar':

                if len(self.values['-TIMEIN1-']) == 0 or len(self.values['-TIMEIN1-']) == 0 or len(self.values['-TIMEOUT1-']) == 0 or len(self.values['-TIMEOUT2-']) == 0:

                    print('Erro: Você esta tentando salvar o horário com um ou mais campos vazios')
                    sg.popup_ok('Erro: Você esta tentando salvar o horário com um ou mais campos vazios!', title='Erro')

                else:

                    '''
                    Se clicar em salvar, formatamos a data registrata no text "data" para algo likely SQL
                    chamamos a funcao de inserir no BD
                    '''

                    data = self.janela.find_element('data').Get()
                    data = data[-4:] + '/' + data[3:5] + '/' + data[:2]  #sql likely
                    #print(data)

                    #abaixo, pega a data de saida, se o campo madrugada estiver validado, adiciono um dia para ficar de um dia para o outro
                    if self.values['madrugada'] == True:
                        # abaixo converto o texto da data em objeto data e deixo ela amigavel a brasileiros
                        date = datetime.strptime(data, '%Y/%m/%d').date() #aqui convertemos a string em obj data
                        data_madrugada = date + timedelta(days=1) #aqui somamos um dia a ela pra o virote da madruga
                        data_madrugada = data_madrugada.strftime('%Y/%m/%d') #aqui convertemos pra texto e jogamos pra montar a string q vai pro bd

                    else:
                        data_madrugada = data

                    string_data_entrada = f'{data} {self.janela.find_element("-TIMEIN1-").Get()}:{self.janela.find_element("-TIMEIN2-").Get()}:00'
                    string_data_saida = f'{data_madrugada} {self.janela.find_element("-TIMEOUT1-").Get()}:{self.janela.find_element("-TIMEOUT2-").Get()}:00'

                    try:
                        #instancio o obj batida do ponto e passo os valores para tratativa
                        batida_ponto = modulo_ponto.Acesso_BD()
                        batida_ponto.inserir_bd(string_data_entrada, string_data_saida)

                        # atualiza a lista e popula com os dados
                        popular_list_box = modulo_ponto.Acesso_BD()
                        lista_populada = popular_list_box.popula_lista()
                        self.janela['-BOX-'].Update(lista_populada)
                        self.janela['-TIMEIN1-'].Update('')  # zera todos os campos
                        self.janela['-TIMEIN2-'].Update('')
                        self.janela['-TIMEOUT1-'].Update('')
                        self.janela['-TIMEOUT2-'].Update('')
                        self.janela['madrugada'].Update(False)
                        self.janela.find_element('-TIMEIN1-').SetFocus()

                        print(f'Registro de ponto inserido com sucesso!')
                        sg.popup_ok(f'Registro de ponto inserido com sucesso!', title='Tudo certo!')

                    except Exception as erro:

                        print(f'Erro ao inserir no BD. Código do erro: {erro}')
                        sg.popup_scrolled(f'Erro na chamada ao módulo do BD. Código do erro: {erro}')


            if self.event in ('Editar'):


                if self.janela.Element('-BOX-').Widget.curselection():  #Aqui eu tentei uma solucao paliativa, manipulei o widget do tkinter para verificar se tem algum componente selecionado
                    indice = self.values['-BOX-'][0] #pega o indice selecionado
                    indice = indice.split(' ') #aqui eu divido o retorno da consulta e pego o index na posicao 0 e a data na posicao 3

                    #abaixo converto o texto da data em objeto data e deixo ela amigavel a brasileiros
                    date = datetime.strptime(indice[3], '%Y/%m/%d').date()
                    data_formatada = date.strftime('%d/%m/%Y')


                    #print(data_formatada, type(date))

                    try:

                       self.janela.find_element('data').Update(data_formatada) #altera a data para formato amigavel para brasileiros

                       data = self.janela.find_element('data').Get()  #altera a data para sql likely
                       data = data[-4:] + '/' + data[3:5] + '/' + data[:2]

                       # abaixo, pega a data de saida, se o campo madrugada estiver validado, adiciono um dia para ficar de um dia para o outro
                       if self.values['madrugada'] == True:
                           # abaixo converto o texto da data em objeto data e deixo ela amigavel a brasileiros
                           date = datetime.strptime(data, '%Y/%m/%d').date()  # aqui convertemos a string em obj data
                           data_madrugada = date + timedelta(days=1)  # aqui somamos um dia a ela pra o virote da madruga
                           data_madrugada = data_madrugada.strftime('%Y/%m/%d')  # aqui convertemos pra texto e jogamos pra montar a string q vai pro bd

                       else:
                           data_madrugada = data


                       #edita a string completa para envio
                       string_data_entrada = f'{data} {self.janela.find_element("-TIMEIN1-").Get()}:{self.janela.find_element("-TIMEIN2-").Get()}:00'
                       string_data_saida = f'{data_madrugada} {self.janela.find_element("-TIMEOUT1-").Get()}:{self.janela.find_element("-TIMEOUT2-").Get()}:00'

                       if len(self.values['-TIMEIN1-']) != 0 or len(self.values['-TIMEIN1-']) != 0 or len(self.values['-TIMEOUT1-']) != 0 or len(self.values['-TIMEOUT2-']) != 0:

                           altera_ponto = modulo_ponto.Acesso_BD()
                           altera_ponto.edita_registro(indice[0], string_data_entrada, string_data_saida)

                           sg.popup_ok(f'Registro do dia {data_formatada} foi editado com sucesso!', title='Sucesso')
                           

                           # atualiza a lista e popula com os dados
                           popular_list_box = modulo_ponto.Acesso_BD()
                           lista_populada = popular_list_box.popula_lista()
                           self.janela['-BOX-'].Update(lista_populada)
                           self.janela['-TIMEIN1-'].Update('')  # zera todos
                           self.janela['-TIMEIN2-'].Update('')
                           self.janela['-TIMEOUT1-'].Update('')
                           self.janela['-TIMEOUT2-'].Update('')
                           self.janela['madrugada'].Update(False)
                           self.janela.find_element('-TIMEIN1-').SetFocus()


                       else:
                           sg.popup_ok('Não editamos o registros. Um ou mais campos não foram preenchidos!', title='Erro')

                    except Exception as erro:
                        sg.popup_scrolled(f'Erro na chamada ao módulo "edita ponto" do BD. Código do erro: {erro}')

                else:
                    sg.popup_ok('Selecione um registro na lista abaixo para Editar!', title='Erro')


            if self.event in ('Exportar'):
                # funcao para salvar as batidas de ponto em relatorio. Caso tenha box2Tux, salva altomaticamente na pasta lá
                arquivo_salvar = sg.popup_get_file('.:Salvar espelho de ponto:.', title='Espelho de ponto',
                                                   save_as=True, no_window=True,
                                                   file_types=(('Arquivos CSV', '*.csv'),), default_extension=".csv",
                                                   initial_folder='./pontos_salvos')

                print(arquivo_salvar)

                if len(arquivo_salvar) >= 4:
                    # se o nome do arquivo for valido, salva
                    try:
                        sg.Print('Montando a lista para ser salva...', text_color='white', background_color='black')
                        lista_espelho = modulo_ponto.Acesso_BD()
                        popular_espelho = lista_espelho.monta_espelho() #monta lista pronta para ser salva no csv

                        # salva a lista em arquivo lendo linha a linha
                        sg.Print(f'Salvando na pasta local..: {arquivo_salvar}', text_color='white', background_color='black')
                        with open(arquivo_salvar, 'w') as arquivo:

                            for linha in popular_espelho:
                                arquivo.write(linha + '\n')

                            arquivo.close()


                        sg.Print('Verificando se o arquivo foi salvo...', text_color='white', background_color='black')

                        if os.path.isfile(arquivo_salvar):
                            sg.Print('Arquivo criado com sucesso!\nCaminho: ' + arquivo_salvar, text_color='white', background_color='black')

                            #verifica se existe modulo samba do box instalado gvfs, caos nao tenha salva so localmente
                            caminho_box = '/run/user/1000/gvfs/dav:host=dav.box.com,ssl=true/dav/'

                            if os.path.exists(caminho_box):
                                sg.Print('Existe uma pasta do Box ativa neste computador. Vamos salvar lá para você na pasta horarios-trabalhados', text_color='white', background_color='black')

                                if os.path.isdir(caminho_box + 'horarios-trabalhados'):
                                    sg.Print('Copiando...', text_color='white', background_color='black')
                                    shutil.copy2(arquivo_salvar, caminho_box + 'horarios-trabalhados')

                                else:
                                    sg.Print('Criando pasta horarios-trabalhados...', text_color='white', background_color='black')
                                    os.mkdir('/run/user/1000/gvfs/dav:host=dav.box.com,ssl=true/dav/horarios-trabalhados')
                                    if os.path.isdir('/run/user/1000/gvfs/dav:host=dav.box.com,ssl=true/dav/horarios-trabalhados'):
                                        sg.Print('Pasta criada', text_color='white', background_color='black')
                                        shutil.copy2(arquivo_salvar, caminho_box + 'horarios-trabalhados')


                            else:
                                sg.Print('Não existe uma pasta do Box ativa nesta máquina. Apenas o arquivo local vai ser salvo.', text_color='white', background_color='black')

                        else:
                            sg.Print('Não foi possível localizar o arquivo.', text_color='white', background_color='black')

                        sg.Print('Finalizando...', text_color='white', background_color='black')
                        time.sleep(8)
                        sg.PrintClose()


                        print(popular_espelho)

                    except OSError:
                        #apresenta um erro pois o box nao aceita symlink entao eu ignoro esse erro
                        sg.Print('Finalizando...', text_color='white', background_color='black')
                        time.sleep(8)
                        sg.PrintClose()

                    except Exception as erro:
                        sg.popup_scrolled(f'Erro ao salvar arquivo de espelho de ponto. Erro: {erro}')






            if self.event in ('Excluir'):

                if self.janela.Element('-BOX-').Widget.curselection(): #Aqui eu tentei uma solucao paliativa, manipulei o widget do tkinter para verificar se tem algum componente selecionado
                    indice = self.values['-BOX-'][0]
                    indice = indice.split(' ')
                    #print(indice[0]) #pega apenas o indice da lista para apagar

                    try:


                        confirmar = sg.PopupOKCancel('Deseja apagar o registro？', title='Apagar registro')

                        if confirmar == 'OK': # se clicar no botão OK, apaga o registro

                            #chama o modulo, instancia a classe e chama o metodo passando pra ele o indice a ser apagado
                            apaga_ponto = modulo_ponto.Acesso_BD()
                            apaga_ponto.apaga_registro(indice[0])

                            # atualiza a lista e popula com os dados
                            popular_list_box = modulo_ponto.Acesso_BD()
                            lista_populada = popular_list_box.popula_lista()
                            self.janela['-BOX-'].Update(lista_populada)
                            self.janela['-TIMEIN1-'].Update('')  # zera todos os campos
                            self.janela['-TIMEIN2-'].Update('')
                            self.janela['-TIMEOUT1-'].Update('')
                            self.janela['-TIMEOUT2-'].Update('')
                            self.janela['madrugada'].Update(False)
                            self.janela.find_element('-TIMEIN1-').SetFocus()

                            sg.popup_animated(image_source='',message=f'REGISTRO <<{indice[0]}>> APAGADO COM SUCESSO...', grab_anywhere=True, keep_on_top=True, alpha_channel=0.9)
                            time.sleep(2)
                            sg.popup_animated(image_source=None) #apaga a mensagem

                    except Exception as erro:

                        sg.popup_scrolled(f'Erro na chamada ao módulo "apaga ponto" do BD. Código do erro: {erro}')

                else:
                    sg.popup_ok('Selecione um registro na lista abaixo para apagar!', title='Erro')


            '''
            Abaixo escutamos todos os campos de hora a ser preenchidos.
            usamos regex para permitir apenas numeros de 0 a 9 nesses campos,
            se for digitado alguma outra coisa ele apaga
            Quando preencher 2 digitos, joga para o proximo ate chegar ao botao
            '''
            if self.event in ('-TIMEIN1-', '-TIMEIN2-', '-TIMEOUT1-', '-TIMEOUT2-'):
                self.janela.find_element(self.event).Update(re.sub('[^0-9]', '', self.values[self.event]))
            if self.event == '-TIMEIN1-' and len(self.janela.find_element(self.event).Get()) == 2:
                self.janela.find_element('-TIMEIN2-').SetFocus()
            if self.event == '-TIMEIN2-' and len(self.janela.find_element(self.event).Get()) == 2:
                self.janela.find_element('-TIMEOUT1-').SetFocus()
            if self.event == '-TIMEOUT1-' and len(self.janela.find_element(self.event).Get()) == 2:
                self.janela.find_element('-TIMEOUT2-').SetFocus()
            if self.event == '-TIMEOUT1-' and len(self.janela.find_element(self.event).Get()) == 2:
                self.janela.find_element('-TIMEOUT2-').SetFocus()
            if self.event == '-TIMEOUT2-' and len(self.janela.find_element(self.event).Get()) == 2:
                self.janela.find_element('Salvar').SetFocus()



if __name__ == '__main__':

    tela_app = Tela_ponto()
    tela_app.Iniciar()