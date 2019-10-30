# LISTA
lista = [1,2,5,8,9, "ggffg",]

print(lista)
print(lista[1])
print(lista[0]+lista[1])


lista2 = list(("novoItem",))
print(lista2)


listaComListas = [['a','b','c'],[2,8,9],[]]
print(listaComListas)
print(listaComListas[0][2])

tamanho = len(lista)
print(tamanho)

# primeiro item da lista

print(lista[-1])

lista3 = [1,2,3,4,5]

lista3 = lista3 + [6,7] #aqui o seis vai pro final

print(lista3)

lista3 = [0] + lista3 #aqui o zero vai pro começo

print(lista3)

lista3.append(8) #append clássico pra add qualquer valor, mas vai pro final

print(lista3)

del(lista3[-1]) #exclui ultimo elemento

print(lista3)

print(10*[0]) # 10 elementos com valor zero


print(50*"-") #imprime 50 vezes um elemento

# LISTA