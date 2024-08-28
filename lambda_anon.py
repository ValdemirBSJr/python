soma = lambda x, y: x + y

print(soma(5, 3))

#ordenar uma lista de tuplas pelo segundo elemento
minha_lista = [('maçã', 2), ('banana', 1), ('laranja', 3)]
minha_lista_ordenada = sorted(minha_lista, key=lambda x: x[1])

print(minha_lista_ordenada)

#usar uma funcao lambda pra ordenar uma lista
lista_mista = [3, 'texto', 1.1, 'a', 25]

lista_ordenada = sorted(
    lista_mista,
    key=lambda x: len(x) if isinstance(x, str) else x
)

print(lista_ordenada)

#ordenar dicionario pelo valor
notas = {'Ana': 9, 'Beto': 7, 'Carlos': 8}

notas_ordenadas = sorted(
    notas.items(),
    key=lambda tupla: tupla[1]
)

print(notas_ordenadas)

#funcao map pode ser aplicada para que uma operação seja aplicada a cada item de uma lista
numeros = [1, 2, 3]
dobrados = list(map(lambda x: x * 2, numeros))
print(dobrados)

#funcao filter para que uma operação seja realizada apenas a elementos que atendam a um criterio
numeros = [1, 2, 3]
pares = list(filter(lambda x: x % 2 == 0, numeros))

print(pares)

#use lambdas para aplicar logica a elementos de coluna
# Criando um DataFrame de exemplo
df = pd.DataFrame({
    'Produto': ["Camiseta", "Calça", "Tênis"],
    'Preco': [100, 150, 200],
})

print(df)

# output:
#     Produto  Preco
# 0  Camiseta    100
# 1     Calça    150
# 2     Tênis    200

df['ComDesconto'] = df['Preco'].apply(lambda x: x * 0.9)
print(df)

# output:
#     Produto  Preco  ComDesconto
# 0  Camiseta    100         90.0
# 1     Calça    150        135.0
# 2     Tênis    200        180.0
