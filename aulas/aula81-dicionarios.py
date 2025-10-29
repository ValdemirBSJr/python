
tel = {
    30342220:'Pericles', 304422021:'Menelau', 30342201:'Tieste'
}

print(tel[304422021])

print(tel)

print(len(tel))

#abaixo retorna so as chaves
print(tel.keys())

#retorna so os valores das chaves
print(tel.values())

print(tel.get(30342201))

del(tel[304422021])

print("Deletei Menelau")

print(tel)

tel[20202020] = 'Romano'

print(tel)

if (30342220 in tel):
    print("Esta chave está contida")
else:
    print("Esta chave não está presente")

