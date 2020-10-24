#!/home/PC/Documents/fonte_sentinela/venv/bin/python /home/PC/Documents/fonte_sentinela/main.py
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#imports
import shelve
import logging
from os import path, listdir, remove

class Manipula_shelve:

    '''
    Classe que irá manipular os arquivos shelve que irão guardar os logins e senhas das páginas
    dos fontes das cidades.
    Teremos um arquivo geral para as fontes e um pra Maceió que não aceita a senha geral.

    :param Nome >>> Nome da cidade/arquivo
    :param login >>> Login do fontes
    :param senha >>> Senha do fontes

    '''


    __slots__ = ['_nome', '_login', '_senha']


    def __init__(self, nome=None, login=None, senha=None):

        self._nome = nome
        self._login = login
        self._senha = senha




    def lista_diretorios(self):

        #listamos o diretorio shelve
        # pega o caminho da aplicação até a pasta shelve
        caminho_shelve = path.join(path.dirname(path.realpath(__file__)), 'shelve/')

        # Se esse caminho for acessível/existir, cria o arquivo e salva as informações
        if path.exists(caminho_shelve):

            try:

                print()
                print('Temos os seguintes arquivos disponíveis..:')
                print()

                #listamos apenas os arquivos e salvc
                lista_arquivos = [arquivo for arquivo in listdir(caminho_shelve) if path.isfile(path.join(caminho_shelve, arquivo))]

                if (len(lista_arquivos)) == 0:

                    print('=' * 100)
                    print('<<Diretório vazio>>')

                else:

                    for arquivo in lista_arquivos:
                        print(arquivo)


                #retornamos o len para validar se existe arquivos na pasta
                return len(lista_arquivos)


            except Exception as Ex:
                print(f'Erro. Não foi possível lista os arquivos na pasta shelve. Cód. erro: {Ex}')
                salva_log = Log_errors(tipo=__file__, erro=Ex)
                salva_log.registra_log()



    def mostra_shelve(self, nome):

        #listamos o diretorio shelve
        # pega o caminho da aplicação até a pasta shelve
        caminho_shelve = path.join(path.dirname(path.realpath(__file__)), 'shelve/')


        # Se esse caminho for acessível/existir, cria o arquivo e salva as informações
        if path.exists(caminho_shelve):

            try:

                abrir_arquivo = path.join(caminho_shelve, nome)

                #caso exista o arquivo, mostramos login e senha salvo
                if path.exists(abrir_arquivo):

                    arquivo = shelve.open(abrir_arquivo)

                    login = arquivo['login']
                    senha = arquivo['senha']

                    arquivo.close()

                    print()
                    print(f'Arquivo selecionado: {nome}.\nLogin atual: {login}.\nSenha atual: {senha}.')

                    #retorna os valores do shelve
                    retorno_shelve = nome + ',' + login + ',' + senha
                    return retorno_shelve


            except Exception as Ex:

                print(f'Não foi possível abrir ou ler o arquivo. Cód. Erro: {Ex}')
                salva_log = Log_errors(tipo=__file__, erro=Ex)
                salva_log.registra_log()




    def criar_shelve(self):

        #pega o caminho da aplicação até a pasta shelve
        caminho_shelve = path.join(path.dirname(path.realpath(__file__)),'shelve/')

        #Se esse caminho for acessível/existir, cria o arquivo e salva as informações
        if path.exists(caminho_shelve):

            try:

                criar_arquivo = shelve.open(path.join(caminho_shelve, self._nome))
                criar_arquivo['login'] = self._login
                criar_arquivo['senha'] = self._senha
                criar_arquivo.close()

                #Aqui verificamos se o arquivo foi criado e retornamos mensagem
                if path.isfile(path.join(caminho_shelve, self._nome)):

                    print(f'Objeto shelve {self._nome} criado com sucesso')


            except Exception as ex:
                print(f'Não foi possível criar o arquivo ou abri-lo. Cód. Erro: {ex}')
                salva_log = Log_errors(tipo=__file__, erro=ex)
                salva_log.registra_log()

        else:

            print('Erro. Não conseguimos achar a pasta shelve.')



    def editar_shelve(self, nome, login, senha):

        #pega o caminho da aplicação até a pasta shelve e verifica o nome do arquivo
        caminho_shelve = path.join(path.dirname(path.realpath(__file__)),'shelve/', nome)

        #verificamos se é um arquivo para poder edita-lo, caso seja inputa novos dados ao arquivo
        if path.isfile(caminho_shelve):

            try:

                arquivo = shelve.open(caminho_shelve)
                arquivo['login'] = login
                arquivo['senha'] = senha
                arquivo.close()

                print(f'O objeto {nome} foi editado com êxito.')

            except Exception as Ex:
                print(f'Erro. Não foi possível abrir ou editar o objeto. Cód. Erro: {Ex}')
                salva_log = Log_errors(tipo=__file__, erro=Ex)
                salva_log.registra_log()


    def apaga_shelve(self, nome):

        #pega o caminho da aplicação até a pasta shelve e verifica o nome do arquivo
        caminho_shelve = path.join(path.dirname(path.realpath(__file__)),'shelve/', nome)

        #verificamos se é um arquivo para poder apaga-lo, caso seja apaga o arquivo
        if path.isfile(caminho_shelve):

            try:
                remove(caminho_shelve)
                print(f'Objeto {nome} apagado com sucesso!')

            except Exception as Ex:

                print(f'Erro ao apagar o arquivo. Cód. Erro: {Ex}')
                salva_log = Log_errors(tipo=__file__, erro=Ex)
                salva_log.registra_log()

    def __str__(self):
        return f'{self._nome},{self._login},{self._senha}'




class Log_errors:

    '''
    Classe para registro de erros da aplicação.
    Serão registrados em um arquivo na pasta log com o nome do módulo que gerou o erro
    :param tipo onde registraremos o nome do mopdulo
    :param erro, onde registraremos o erro
    '''

    __slots__ = ['_tipo', '_erro']

    def __init__(self, tipo=None, erro=None):

        self._tipo = tipo
        self._erro = erro

    def registra_log(self):

        tipo_formatado = self._tipo.split('/')
        tipo_formatado = tipo_formatado[-1] #pega o ultimo valor
        tipo_formatado = tipo_formatado[0:-3] #exclui o .py

        caminho_log = path.join(path.dirname(path.realpath(__file__)), 'log/') + tipo_formatado + '.log'

        logger = logging.getLogger(self._tipo)
        hdlr = logging.FileHandler(caminho_log)
        formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.ERROR)

        logger.error(self._erro)




if __name__ == '__main__':

    print('=' * 100)
    print()
    print('Bem-vindo ao gerenciador de senhas e logins com o SHELVE!')
    print()
    print('=' * 100)
    print()

    marcador = True

    while marcador:

        print()
        print('O que gostaria de fazer agora? Digite um dos números abaixo')
        print()

        escolha = input('| 1 | -> CRIAR SHELVE\n| 2 | -> EDITAR SHELVE\n| 3 | -> EXCLUIR SHELVE\n| 4 | -> LISTAR SHELVE\n| 5 | -> EXIBIR SHELVE\n| 6 | -> FINALIZAR\n').strip()



        if escolha == '1':

            print('=' * 100)
            nome = input('Qual o nome do arquivo?\nDica: Coloque o nome ou sigla da cidade.\n').strip().upper()
            login = input('Digite o login da página (Não pode haver erros).\n').strip()
            senha = input('Digite a senha da página (Não pode haver erros).\n').strip()

            if nome != '' and login != '' and senha != '':

                arquivo = Manipula_shelve(nome=nome, login=login, senha=senha)
                arquivo.criar_shelve()

            else:

                print('Um dos atributos está vazio e não é válido! Tente novamente.')



        elif escolha == '2':

            print('=' * 100)


            arquivo = Manipula_shelve()
            retorno_diretorio = arquivo.lista_diretorios()


            if retorno_diretorio == 0:

                print()
                print('Tente inserir um objeto para realizar a operação.')

            else:

                arquivo_editavel = input('Qual dos arquivos gostaria de editar?\n').strip().upper()

                arquivo.mostra_shelve(arquivo_editavel)

                print()
                print(f'Editando: {arquivo_editavel}\n')

                login = input(f'Digite o novo login para {arquivo_editavel}:\n').strip()
                senha = input(f'Digite a nova senha para {arquivo_editavel}:\n').strip()

                arquivo.editar_shelve(arquivo_editavel, login, senha)

                arquivo.mostra_shelve(arquivo_editavel)



        elif escolha == '3':

            arquivo = Manipula_shelve()
            retorno_diretorio = arquivo.lista_diretorios()

            if retorno_diretorio == 0:

                print()
                print('Tente inserir um objeto para realizar a operação.')

            else:

                arquivo_apagar = input('Qual desses arquivos gostaria de apagar?\n').strip().upper()

                print('=' * 100)
                escolha_apagar = input(f'Arquivo selecionado: {arquivo_apagar}.\nTem certeza? [s] para sim e [n] para não.\n').strip().lower()

                if escolha_apagar == 's':

                    arquivo.apaga_shelve(arquivo_apagar)

                elif escolha_apagar == 'n':
                    print('OK então. Nada feito!')

                else:
                    print('Opção inválida. Não foi possível apagar o arquivo.')


        elif escolha == '4':

            arquivo = Manipula_shelve()
            arquivo.lista_diretorios()



        elif escolha == '5':

            print()

            arquivo = Manipula_shelve()

            retorno_diretorio = arquivo.lista_diretorios()

            if retorno_diretorio == 0:

                print()
                print('Tente inserir um objeto para realizar a operação.')

            else:

                print()
                arquivo_exibido = input('Qual objeto shelve gostaria de visualizar?').strip().upper()

                retorn = arquivo.mostra_shelve(arquivo_exibido)



        elif escolha == '6':

            print('=' * 100)
            print('Até a próxima!')
            marcador = False


        else:
            print('Opção inválida, tente novamente!')



