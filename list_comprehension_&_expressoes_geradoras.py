#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra
import locale
'''
exemplo de list comprehension: Se quiser computar o quadrado de uma lista

expressões geradoras servem pra fazer a mesma coisa,
mas um passo na iteração de cada vez, para não dar stack overflow
'''

lista = [1,2,3,4,5,6]

quadrado = [x**2 for x in lista]
print(quadrado)

#se quiser o quadrado apenas dos numeros divisiveis por 2
so_pares = [x**2 for x in lista if x % 2==0]
print(so_pares)

#expressões geradoras:
raiz = ((x, x**0,5) for x in lista)

print(next(raiz))
print(next(raiz))

#LIST

#[expr for item in lista]
# Aplique a expressão expr em cada item da lista

# [expr for item in lista if cond]
# Aplique a expressão expr em cada item da lista caso a condição cond seja satisfeita.

lista_numerica = [1, 2, 3, 4, 5, 6, 7, 8, 9]
lista_texto = ['predo', 'toinho', 'ocrido']

#multiplica todos os valores por 2
print([item*2 for item in lista_numerica])
#deixa tudo em caixa alta
print([str(item).upper() for item in lista_texto])

#mostra so os pares
print([item for item in lista_numerica if item % 2 ==0])

#ifs encadeados. pegar os multiplos comuns de 2 e 3
print([numero for numero in lista_numerica if numero % 2 == 0 if numero % 3 ==0])

#[resultado_if if expr else resultado_else for item in lista]
#para cada item da lista, aplique o resultado resultado_if se a expressão expr for verdadeira, caso contrário, aplique resultado_else
print(['PAR' if numero % 2 ==0 else 'IMPAR' for numero in lista_numerica])
print([numero*2 if numero ==2 else numero*1 for numero in lista_numerica])

##############################################################################################################
#DICT

#{chave: valor for elemento in iteravel}
dicionario = {elemento: elemento*2 for elemento in range(6)}
print(dicionario)

lista_carros = ['Ferrari', 'Lamborguini', 'Porsche']
dicionario_carros = {f'{elemento.lower()}': f'Montadora: {elemento.upper()}' for elemento in lista_carros}
print(dicionario_carros)

#iterar sobre outro dict com o metodo items()
locale.setlocale(locale.LC_MONETARY, 'pt_BR.utf8')
carros_esportivos = {
    'ferrari': 1299000,
  'lamborghini': 1100000,
  'porsche': 759000
}
dicionario_saida_ce = {chave: f'{chave.upper()}: {locale.currency(valor, grouping=True)}' for chave, valor in carros_esportivos.items()}
print(dicionario_saida_ce)

#Podemos adicionar uma expressão condicional em três posições distintas:
#{chave if condicao: valor for elemento in iteravel}
#{chave: valor if condicao for elemento in iteravel}
#{chave: expressao for elemento in iteravel if condicao}

#filtrar carros esportivos acima de 1 milhao
carros_milionarios = {f'{chave.upper()}: {locale.currency(valor, grouping=True)}' for chave, valor in carros_esportivos.items() if valor > 1000000}
print(carros_milionarios)

vergonha_de_ser_mais_barato = {


    f'{chave.upper()}: {locale.currency(valor, grouping=True)}'
    if valor > 1000000 else f'{chave.upper()}-valor-abaixo: Valor abaixo de R$ 1.000.000,00'
    for chave, valor in carros_esportivos.items()
}
#se o valor do carro for abaixo de 1 milhao nao coloca o valor
print(vergonha_de_ser_mais_barato)

numeros = {numero for numero in range(0,11)}
chaves = ['pares', 'impares']
filtros = {chaves[0]: {numero for numero in numeros if not numero % 2}}
filtros[chaves[1]] = {numero for numero in numeros if numero % 2}

#filtros.setdefault(chaves[1], {numero for numero in numeros if numero % 2})

#filtros = {
#    keys[0]: {numero for numero in numeros if not numero % 2},
#    keys[1]: {numero for numero in numeros if numero % 2}
#}

print(filtros)

######################################################################################################
servidores = {'192.168.0.1': {'SERVICO': 'PRI', 'HOSTNAME': 'localhost', 'MODELO': 'x86'}}
caminho = 'C:\\Users\\Usuario\\Documents\\PycharmProjects\\whatchdog_pgp\\pasta_pra_onde_vai\\'
data_atual = datetime.now()
pasta_mes = data_atual.strftime('%B-%Y').upper()
pasta_dia = data_atual.strftime('%d.%m.%Y')
data_arquivo = data_atual.strftime('%Y%m%d')
caminho_completo_arquivos_esperados = [f'{caminho}log_{valor["SERVICO"]}\\{pasta_mes}\\{pasta_dia}\\{data_arquivo}_{chave}.txt' for chave, valor in servidores.items()]

lista1 = ['1', '2', '3']
lista2 = ['1', '4', '6']

itens_faltando = [item for item in lista1 if item not in lista2]
itens_repetidos = [item for item in lista1 if item in lista2]

caminhos_dos_arquivos = ['/home/caminho/arquivo1', '/home/caminho/arquivo2']
caminho_splitado = [caminho.split('/') for caminho in caminhos_dos_arquivos]
nome_formatado = [str(formatado[1] + '-> Número do arquivo: ' + formatado[3][-1]) for formatado in caminho_splitado]

carros = {
    'sandero': {'TIPO': 'popular', 'ANO': 2017},
    'camaro': {'TIPO': 'esportivo', 'ANO': 2020}, 
    'onix': {'TIPO': 'popular', 'ANO': 2021}, 
}

lista_montada_formatada = [f'{carro}: Ano de fabricação: {dado["ANO"]}. Estilo: {dado["TIPO"]}' for carro, dado in carros.items()]

# listando todos arquivos de 4 pastas, pegando caminho completo:
pastas = ['/home/caminho/pasta1', '/home/caminho/pasta2']
caminho_completo_arquivos_presentes = [os.path.join(pasta, arquivo)
                      for pasta in pastas
                      for arquivo in os.listdir(pasta)
                      if os.path.isfile(os.path.join(pasta, arquivo))]

