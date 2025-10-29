# iterando listas em python, iterar é percorrer todos os itens

lista_nums = [100, 200, 300, 400]

lista_indice = [0, 1, 2, 3] # estes números dizem respeito aos índices da lista pode ser tbm lista_indice = range(0,4)

for item in lista_indice:
    lista_nums[item] += 1000
print(lista_nums)


for item in range(4):
    lista_nums[item] -= 1000
print(lista_nums)

#agora pode ser alterado quantidade
lista_variavel = [100, 200, 300, 400, 500, 600, 700]

for item in range(len(lista_variavel)):
    lista_variavel[item] += 1000
print(lista_variavel)

#função enumerate. Ela já atribui altomaticamente um índice
lista_enum = [100, 200, 300]
for idx, item in enumerate(lista_enum):
    lista_enum[idx] += 1000
print(lista_enum)

'''
FATIANDO LISTAS

'''

# lista[ X: Y: Z]  X = comecar(0) | Y = aonde para(comprimento - len() | Z = passo, intervalo de avanço

listaFatiar = ['P', 'Y', 'T', 'H', 'O', 'N']

print(listaFatiar[::-1])

print(listaFatiar[::3])

print(listaFatiar[:4:1])


'''
TRABALHANDO COM CONTEÚDOS DE LISTAS

'''

listaAdd = ['bbb', 'ccc']

listaAdd.append('eee')

print(listaAdd)

# pra inserir um elemento em uma posição especifica, usar insert

listaAdd.insert(0, 'aaa')

print(listaAdd)

#tem essa forma também para substituir
listaAdd[1] = 'bbba'

print(listaAdd)

listaAdd.pop() # remove/retorna ultimo elemento da lista

print(listaAdd)

listaAdd.pop(0) # exclui o indice zero

print(listaAdd)

listaAdd.insert(0, 'aaa')
listaAdd.insert(3, 'ddd')

print(listaAdd)

#pra apagar intervalos

del(listaAdd[:2:])

print(listaAdd)

print(listaAdd.count('ddd')) #Aqui conta quantas vezes tem um elemento

print(len(listaAdd)) #Aqui conta quantos elementos tem

print(listaAdd.index('ddd')) #retorna o indice do valor


# contém e não contém ==> IN e NOT IN

# E => AND | OU => OR

listadeVerificacao = [0, 1, 2, 3, 4]

if (1 in listadeVerificacao):
    print("O 1 está contido.")

if(5 not in listadeVerificacao):
    print("O 5 não está contido.")

if ((1 and 2) or (4 and 5) in range(1, 6)):
    print("Verdadeiro")
else:
    print("Falso")




cores = ["azul", "amarelo", "vermelho", "branco"]

while True:
    cor = input("Digite o nome de uma cor ou então,"
                " 0 para sair do programa..: ").lower() # lover transforma o input em minusculas
    if (cor == "0"):
        print("Tchau!")
        break
    if cor in cores:
        print("Essa cor está contida!")
    else:
        print("Essa cor NÃO está contida!")