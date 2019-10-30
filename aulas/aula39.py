a = 1
b = 2

def soma_num(var1, var2):
    s = var1+ var2
    return s

def imprime(x_vezes):
    for i in range(x_vezes):
        print(i)


print(soma_num(a, b))

valor_a_ser_impresso = int(input("Digite o valor inicial do contador..:"))

imprime(valor_a_ser_impresso)

s = "O número digitado é par" if valor_a_ser_impresso % 2 == 0 else "O número digitado é impar."
print(s)

x = 0
while(x<10):
    print(x)
    x += 1;
else:
    print("else")


for c in "python":
    print(c)

i_vezes = 2
for i in range(i_vezes):
    print(i)

print(list(range(0,10,1))) # lista de zero a 10 de um a um