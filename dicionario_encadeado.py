dicionario_aninhado = {

    'dicionario1': {'chaved1': 'valord1'},
    'dicionario2': {'chaved2': 'valord2', 'idade': 23},

}

#imprime um valor em específico
print(dicionario_aninhado['dicionario1'])
print(dicionario_aninhado['dicionario1']['chaved1'])
print(dicionario_aninhado['dicionario2']['idade'])

#adiciona uma nova chave
dicionario_aninhado['dicionario3'] = {}

dicionario_aninhado['dicionario3']['chaved3'] = 'valord3'

print(dicionario_aninhado)

#outra forma para adicionar
dicionario_aninhado['dicionario4'] ={'chaved4': 'valord4'}

print(dicionario_aninhado)

#adicionando uma entrada a mais na chave
dicionario_aninhado['dicionario4'].update({'idade': 44})

print(dicionario_aninhado)

#apagando um elemento na chave
del dicionario_aninhado['dicionario2']['idade']

print(dicionario_aninhado['dicionario2'])

#apagando uma chave
del dicionario_aninhado['dicionario4']

print(dicionario_aninhado)

#percorrendo os elementos
for dic_ID, dic_INFO in dicionario_aninhado.items():
    print(f'ID do dicionário: {dic_ID}.')

    for chave in dic_INFO:
        print(f'Chave do dicionário: {chave} | Valor:{dic_INFO[chave]}') #se botar so o valor dict_INFO, ele tras tudo
