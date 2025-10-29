idade =  int(input("Digite sua idade..:"))

if(idade<=0):
    print("A sua idade não pode ser menor de zero!")
else:
    if(idade>150):
        print("A sua idade não pode ser maior de 150 anos!")
    else:
        if(idade < 18):
            print("Você precisa ter mais de 18 anos!")
        if (18 < idade < 150):
            print("Você tem a idade certa, está apto!")
