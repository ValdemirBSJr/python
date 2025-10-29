"""

MANIPULAÇÃO DE DADOS, AULA 24,25

"""

num_int = 5
num_dec = 7.3
val_str = "Um texto qualquer"

#abaixo tres formas de concatenar string
print("O valor de nossa variável é: ", num_int)
print("O valor da variável inteira é: %i" %num_int)
print("O valor da nossa variável inteira é: " + str(num_int))

#abaixo tres formas de concatenar string com decimal
print("Concatenando decimal: ", num_dec)
print("Concatenando por marcador a decimal: %.2f" %num_dec)
print("Concatenando transformando e string: " + str(num_dec))

#concatenar textos

print("O valor da variável é: ", val_str)
print("O valor por parametro: %s" %val_str)
print("O valor concatenado: " + val_str)