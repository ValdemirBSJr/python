acao = int(input("Digite '1' para sim e digite '2' para não."))

if(acao==1):
    print("Você disse que sim!")
else:
    if(acao==2):
     print("Você disse que não!")
    if(acao>2):
        print("Você digitado não é '1' e nem '2'")