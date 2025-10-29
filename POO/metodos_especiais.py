#!/home/valdemir/e38/bin/python3.8
# -*- coding: utf-8 -*-
#Author: Valdemir Bezerra

class Filmes:
    __slots__ = ['_titulo', '_diretor', '_duracao']
    def __init__(self, titulo, diretor, duracao):
        self._titulo = titulo
        self._diretor = diretor
        self._duracao = duracao

    def __str__(self):
        return f'Título: {self._titulo}. Diretor: { self._diretor}. Duracao: {self._duracao}'

    def __len__(self):
        return self._duracao

    def len(self):
        return  print(f'Duração do filme: {self._duracao}.')

filme = Filmes(titulo='A noite dos mortos-vivos', diretor='George A. Romero', duracao=96)

print(str(filme))

print(len(filme))

filme.len()

