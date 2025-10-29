

print("Antes do laço")

for item in range(10):
    print(item)
    if(item == 6):
        print("A condição retornou true")
        break #finaliza o laço de repetição

print("Fim do laço")

print("continue com while")

i = 0

while(i < 10):
    i +=1
    if(i % 2 == 0):
        continue # Ele retorna a realizar o laço
    print(i)

else:
    print("else")
print("fim")