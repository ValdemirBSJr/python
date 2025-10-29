#!/home/datacenter/.virtualenvs/k37/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

'''
Vamos tentar abrir um arquivo que não existe
mandatario tentar abrir ele antes, pois caso de erro(ele não existe)
não será tratado no finally
'''

def divide(a, b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Inputs inválidos!') from e

x,y = 6,2

try:
    resultado = divide(x,y)
except ValueError:
    print('Inputs invalidos meu!')
else:
    print(f'Resultado é {resultado}')

##################################################

try:
    x = int(input("Digite um número: "))
    y = int(input("Digite outro número: "))
    if y == 0:
        raise RuntimeError("Divisão por zero não é permitida.")
    resultado = x / y
    print(f"O resultado é: {resultado}")
except RuntimeError as e:
    print(f"Erro de execução: {e}")
except ValueError:
    print("Erro: Entrada inválida! Por favor, digite um número.")

#O bloco else é executado apenas se o bloco try não gerar nenhuma exceção. 
#Util para executar o codigo que deve rodar apenas quando nao há erros

try:
    x = int(input("Digite um número: "))
    y = int(input("Digite outro número: "))
    resultado = x / y
except ZeroDivisionError:
    print("Erro: Não é possível dividir por zero!")
except ValueError:
    print("Erro: Entrada inválida! Por favor, digite um número.")
else:
    print(f"O resultado é: {resultado}")

#O bloco finally é executado independentemente de qualquer exceção que ocorra. 
#Isso é útil para liberar recursos ou executar ações de limpeza

try:
    x = int(input("Digite um número: "))
    y = int(input("Digite outro número: "))
    resultado = x / y
except ZeroDivisionError:
    print("Erro: Não é possível dividir por zero!")
except ValueError:
    print("Erro: Entrada inválida! Por favor, digite um número.")
else:
    print(f"O resultado é: {resultado}")
finally:
    print("Execução finalizada.")


#Para gerar uma exceção e parar a execução do código, utilizamos a palavra-chave raise. 
#Isso nos permite lançar uma exceção em qualquer ponto do nosso código, interrompendo sua execução imediatamente.
def dividir(a, b):
    if b == 0:
        raise ValueError("O divisor não pode ser zero!")
    return a / b

try:
    resultado = dividir(10, 0)
    print(resultado)
    
except ValueError as e:
    print(f"Erro: {e}")

#podemos criar nossas próprias exceções personalizadas
class DivisaoPorZeroError(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

def dividir(a, b):
    if b == 0:
        raise DivisaoPorZeroError("Não é possível dividir por zero!")
    return a / b

try:
    resultado = dividir(10, 0)
except DivisaoPorZeroError as e:
    print(f"Erro: {e.mensagem}")

