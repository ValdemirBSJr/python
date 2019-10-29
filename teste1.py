def msg(mens):
    print("O valor digitado foi: " +mens)

mensagem = input("Digite um nome: ")

msg(mensagem)

mensagem2 = input("Digite para forma direta..: ")

print("Foi digitado: " + mensagem2)

print("O tamanho do primeiro nome foi: " + str(len(mensagem)))

total = 0

for num in range(101):
    total = total + num

print(total)