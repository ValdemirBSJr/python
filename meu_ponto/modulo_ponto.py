#!/home/valdemir/Documentos/PYTHON-PROJETOS/meu_ponto/venv/bin/python
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import sqlite3
import os
from datetime import datetime, timedelta


class Acesso_BD:

    '''
    Este modulo é a classe de trabalho com o BD
    '''

    __slots__ = ['_data_marcacao', '_hora_entrada', '_hora_saida', '_mensagem']

    def __init__(self, data_marcacao=None, hora_entrada=None, hora_saida=None, mensagem=None):

        self._data_marcacao = data_marcacao
        self._hora_entrada = hora_entrada
        self._hora_saida = hora_saida
        self._mensagem = mensagem


    def __str__(self):
        #retorna string ao inves do objeto nas mensagens
        return f'{self._mensagem}'



    def conecta_ao_bd(self) -> str:

        #verifica se existe um bd, caso nao haja, se cria um

        try:

            if os.path.exists('marcacoes.db'):

                self._mensagem = 'Tudo OK!'
                return self._mensagem
            else:
                dbase = sqlite3.connect('marcacoes.db')

                c = dbase.cursor()

                dbase.execute('''CREATE TABLE IF NOT EXISTS ponto_gravado(
                            Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            Horario_in TEXT NOT NULL,
                            horario_out TEXT NOT NULL
                            
                )''')


                dbase.commit()


                self._mensagem = 'Tudo OK!'
                #print(str(dbase))
                return self._mensagem

        except Exception as erro:
            self._mensagem = f'Não foi possível acessar ou criar o Bd! Erro: {erro}.'
            return self._mensagem





    def inserir_bd(self, entrada: str, saida: str) -> str: #Se fosse um dicionario>>> opts: dict=None
        #funcao para inserir um registro no BD
        try:
            if self.conecta_ao_bd() == 'Tudo OK!': #verifico se o BD existe e se esta acessível

                dbase = sqlite3.connect('marcacoes.db')
                c = dbase.cursor()
                #print(f'Mandar STRING ADD AO BANCO INSERT!{entrada} {saida}')
                sql_insert = 'INSERT INTO ponto_gravado (Horario_in, horario_out) VALUES (?, ?)'
                registro = [entrada, saida]
                c.execute(sql_insert, registro)
                dbase.commit()


                print(f'Registro efetuado com sucesso! \n{c.lastrowid}')
                return f'Quantidade de registro(s) efetuado(s): {c.lastrowid}'

        except Exception as erro:
            print(f'Oops: Erro ao inserir no BD. Erro: {erro}')
            return f'Oops: Erro ao inserir no BD. Erro: {erro}'


    def popula_lista(self) -> list:
        #iremos retornar uma lista do BD e populamos a listBox
        # funcao para inserir um registro no BD
        try:
            if self.conecta_ao_bd() == 'Tudo OK!':  # verifico se o BD existe e se esta acessível

                dbase = sqlite3.connect('marcacoes.db')
                c = dbase.cursor()
                # print(f'Mandar STRING ADD AO BANCO INSERT!{entrada} {saida}')
                sql_select = 'SELECT * FROM ponto_gravado'
                c.execute(sql_select)
                data = c.fetchall()
                dbase.commit()

                #edito a data para ficar com apresentacao melhor, criando uma nova lista para nao trabalhar com as tuplas retornadas e formatando a data para ficar amigável para brasileiros
                data_formatada = []
                for indice in range(len(data)):

                    #converto o formato da data
                    data_entrada = datetime.strptime(data[indice][1], '%Y/%m/%d %H:%M:%S')
                    data_entrada_input = data_entrada.strftime('%d/%m/%Y %H:%M:%S') #aqui convert em string pra salvar

                    data_saida = datetime.strptime(data[indice][2], '%Y/%m/%d %H:%M:%S')
                    data_saida_input = data_saida.strftime('%d/%m/%Y %H:%M:%S')

                    data_diferenca = abs((data_saida-data_entrada).total_seconds()) #aqui faço o calculo das horas trabalhadas
                    data_diferenca = (data_diferenca / 60)/60

                    data_formatada.append(f'{data[indice][0]} - ENTRADA: {data_entrada_input} | SAÍDA: {data_saida_input} | HORAS TRABALHADAS: {data_diferenca:.2f}')

                #print(data_formatada)


                #print(f'Consulta efetuada!')
                return data_formatada

        except Exception as erro:
            print(f'Oops: Erro ao consultar BD. Erro: {erro}')
            return f'Oops: Erro ao consultar BD. Erro: {erro}'


    def monta_espelho(self) -> list:
        #iremos retornar uma lista do BD para jogar no csv

        try:
            if self.conecta_ao_bd() == 'Tudo OK!':  # verifico se o BD existe e se esta acessível

                dbase = sqlite3.connect('marcacoes.db')
                c = dbase.cursor()
                sql_select = 'SELECT * FROM ponto_gravado'
                c.execute(sql_select)
                data = c.fetchall()
                dbase.commit()

                # monto no formato de tabela para ser aberto no excel, csv
                data_formatada = ['ÍNDICE;ENTRADA;SAÍDA;TOTAL DE HORAS TRABALHADAS']
                for indice in range(len(data)):

                    #converto o formato da data
                    data_entrada = datetime.strptime(data[indice][1], '%Y/%m/%d %H:%M:%S')
                    data_entrada_input = data_entrada.strftime('%d/%m/%Y %H:%M:%S') #aqui convert em string pra salvar

                    data_saida = datetime.strptime(data[indice][2], '%Y/%m/%d %H:%M:%S')
                    data_saida_input = data_saida.strftime('%d/%m/%Y %H:%M:%S')

                    data_diferenca = abs((data_saida-data_entrada).total_seconds()) #aqui faço o calculo das horas trabalhadas
                    data_diferenca = (data_diferenca / 60)/60

                    data_formatada.append(f'{indice + 1};{data_entrada_input};{data_saida_input};{data_diferenca:.2f}')

                #print(data_formatada)


                #print(f'Consulta efetuada!')
                return data_formatada

        except Exception as erro:
            print(f'Oops: Erro ao consultar BD. Erro: {erro}')
            return f'Oops: Erro ao consultar BD. Erro: {erro}'


    def edita_registro(self, indice:str, entrada: str, saida:str) -> str:
        #funcao que edita o registro existente
        try:
            if self.conecta_ao_bd() == 'Tudo OK!': #verifico se o BD existe e se esta acessível

                dbase = sqlite3.connect('marcacoes.db')
                c = dbase.cursor()
                sql_update = 'UPDATE ponto_gravado SET Horario_in=?, horario_out=? WHERE Id=?'
                registro = [entrada, saida, indice]
                c.execute(sql_update, registro)
                dbase.commit()


                print(f'Registro efetuado com sucesso! \n{c.lastrowid}')
                return f'Quantidade de registro(s) efetuado(s): {c.lastrowid}'

        except Exception as erro:
            print(f'Oops: Erro ao inserir no BD. Erro: {erro}')
            return f'Oops: Erro ao inserir no BD. Erro: {erro}'


    def apaga_registro(self, indice: str) -> str:
        # funcao para inserir um registro no BD
        try:
            if self.conecta_ao_bd() == 'Tudo OK!':  # verifico se o BD existe e se esta acessível

                dbase = sqlite3.connect('marcacoes.db')
                c = dbase.cursor()
                sql_delete = 'DELETE FROM ponto_gravado WHERE id=?'
                registro = [indice]
                c.execute(sql_delete, registro)
                dbase.commit()

                print(f'Registro apagado com sucesso! Qtde: \n{c.lastrowid}')
                return f'Registro apagado com sucesso!\nQuantidade de registro(s) apagados(s): {c.lastrowid}'

        except Exception as erro:
            print(f'Oops: Erro ao apagar no BD. Erro: {erro}')
            return f'Oops: Erro ao apagar no BD. Erro: {erro}'



if __name__ == '__main__':

    teste_conexao = Acesso_BD()
    teste_conexao = teste_conexao.popula_lista()
    print(str(teste_conexao))
    #teste_conexao.inserir_bd('lala', 'lolo')
    pass







