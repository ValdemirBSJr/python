#!python3
#coding: utf-8
#author: valdemir


class Pessoa:
    #inicializa um objeto com os valores padrão sempre que a classe pessoa é chamada
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade # self aqui faz referencia, se torna um atributo de um objeto

    def imprimir_nome(self):
        print(self.nome)

    def imprimir_idade(self):
        print(self.idade)


class Conta:

    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero

class ContaEspecial(Conta):
    #vai herdar de conta
    def __init__(self, cliente, numero, limite=0):
        Conta.__init__(self, cliente, numero)
        self.limite = limite


p = Pessoa('Valdemir', 33)

#print(p.nome)
#print(p.idade)

p.imprimir_nome()
p.imprimir_idade()

conta = ContaEspecial(p.nome, '1234', 100)
print(conta.limite)
print(conta.cliente)
print(conta.numero)

#Se voce fizer o de baixo, da erro pois nao ha 'limite' na classe conta e sim na herdada
#conta = Conta('Valdemir','1234',100)
#print(conta.limite)