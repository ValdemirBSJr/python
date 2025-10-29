# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

import os
import sqlite3

#Se existir um bd, apaga ele
os.remove('morador.db') if os.path.exists('morador.db') else None

#Criar uma conexao com um bd, se nao existir cria o arquivo
con = sqlite3.connect('morador.db')

print(type(con))

#cria um cursor para que voce possa percorrer o bd
cur = con.cursor()

print(type(cur))

##########################################3

# Criacao da tabela

# criamos uma tabela dentro do bd
sql_create = 'CREATE TABLE apartamento (id integer primary key, morador varchar(100), andar varchar(50))'

# executa a criacao com o cursor
cur.execute(sql_create)

########################################

# Sentenca SQL para inserir registros na tabela criada. Assim é necessario passar o id
#sql_insert = 'INSERT INTO apartamento VALUES (?, ?, ?)'

#dados que serao inseridos
#registros = [

#     (1, 'Ana Paula', 'Térreo'),
#     (2, 'Paulo Vitor', 'Primeiro andar'),
#     (3, 'Adalto Farias', 'Segunda andar'),
#     (4, 'Maria Luiza', 'Terceiro andar')
# ]

#Usando essa sintaxe vc nao precisa por o id, ele poe altomaticamente
sql_insert = 'INSERT INTO apartamento (morador, andar) VALUES (?, ?)'

registros = [

     ('Ana Paula', 'Térreo'),
     ('Paulo Vitor', 'Primeiro andar'),
     ('Adalto Farias', 'Segunda andar'),
     ('Maria Luiza', 'Terceiro andar')
 ]

#Inserir registros
for registro in registros:
    cur.execute(sql_insert, registro)

 #Para gravar a transacao, necessario commit ou nao sao gravados
con.commit()

#####################################################################

#vamos selecionar registros para exibir
sql_select = 'SELECT * FROM apartamento'

#executar o comando
cur.execute(sql_select)

#recuperar os dados
dados = cur.fetchall()

for dado in dados:
    print(dado)

#outra forma de exibir
for dado in dados:
    print(f'Id: {dado[0]}. Morador: {dado[1]}. Andar: {dado[2]}.')

#fechando o banco
con.close()