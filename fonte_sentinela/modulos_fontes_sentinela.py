#/home/valdemir/Documentos/PYTHON-PROJETOS/fonte_sentinela/venv/bin/python /home/valdemir/Documentos/PYTHON-PROJETOS/fonte_sentinela/main.py
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra




class Lista_Site_Fontes:

    '''
    Instanciamos todas os sites das fontes
    Classe que se comporta como dicionario
    :parameter chave >>> chave das fontes
    :param valor >>> valores que contem os endereços
    '''

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def __repr__(self):
        return repr(self.__dict__)

    def popular(self, *args, **kwargs):
        #update
        return self.__dict__.update(*args, **kwargs)

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    #def __unicode__(self):
        #return unicode(repr(self.__dict__))





if __name__ == '__main__':



    objeto = Lista_Site_Fontes()
    #objeto['chave'] = 'valor'

    lista = {
        'RCE': 'http://fontes.rce.virtua.com.br/',
        'NTL': 'http://fontes.ntl.virtua.com.br/',
        'MCO': 'http://fontes.mco.virtua.com.br/',
        'JPA': 'http://fontes.jpa.virtua.com.br/',
        'CGE': 'http://fontes.cge.virtua.com.br/',
        'FLA': 'http://fontes.fla.virtua.com.br/',
        'TSA': 'http://fontes.tsa.virtua.com.br/',
    }

    objeto.popular(lista)

    print(objeto)


