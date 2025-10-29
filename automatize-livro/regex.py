#!python3
#coding: utf-8
#author: valdemir

import re

#O r antes é pra informar que a string é pura 'raw_string' aí nao preciso botar duas barras \\ pra representar uma
#passamos aqui o padrao que queremos achar
#parenteses criam grupos
numeroFoneRegex = re.compile(r'(\d\d)-(\d\d\d\d\d-\d\d\d\d)')

# O metodo search busca o padrão dentro do texto
busca = numeroFoneRegex.search("Meu numero de telefone é 83-99964-8878, mas tem 83-99171-2024")

#O group mostra o match
print("Número achado: " + busca.group())
print("Seu DDD é: " + busca.group(1)) #retorna tupla o id é o grupo criado pelo parenteses

#outra forma de fazer nomeado
codigoArea, numero = busca.groups()

print("Número achado: " + codigoArea)
print("Seu DDD é: " + numero)
