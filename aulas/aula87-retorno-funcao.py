def soma():
    return 10


print(soma())

def multiplica(x, y):
    num = x * y
    return num

print(multiplica(2, 3))

def funcao():
    return 1, 2

a, b = funcao()

print(a)
print(b)

def potencia(x):
    quadrado = x ** 2
    cubo = x **3

    return quadrado, cubo

q,c = potencia(10) #potencia de 10 nos valores passados

print(q)
print(c)

def lista_de_argumentos(*lista): #asterisco pra indicar que vai passar uma lista de parametros
    print(lista)


lista_de_argumentos(1, 2, 3, 4)

def lista_de_dicionario(**dicionario):
    print(dicionario)

lista_de_dicionario(a=1,b=2,c=3)