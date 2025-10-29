#
# --- STRINGS --- #

s1 = """ LALALA
LELELE
LILI"""

s2 = "Ao redor do buraco, tudo é bêra..."

print(s1)

# para o python, toda a string é uma lista imutável

print(s1[0:7:1])

print(s2[19:34:1])

for c in range(122):
	print(str(c) + " - " + chr(c))


print(ord("d"))

# quebrar strings:

s = "Lista de caracteres"

lista = s.split(" ")

print(lista)

print(lista[0] + " " + lista[2])

lista2 = s.replace("de", "")

print(lista2)

s = "Iterando strings"
indice = 0

for c in s:
    print(c)

while indice < len(s):
    print(indice, s[indice])
    indice+=1


# forma mais simples de iterar com indices
#k = key(chave e v = valor
# a função enumerate atribui um indice(k) ao valor(v)
for k,v in enumerate(s):
    print(k, v)

