#! /home/PGP_SRV/venv/bin/python
import os
import re
import sys
import shutil
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

caminho = '/home/'

lista_arquivos = []

#Pasta de salvamento raiz dos logs do PGP
PASTA_LOG = 'PGP_SRV/'

#comeca com PGP, tem 3 a 7 caracteres seguido de _ e 8 digitos mais - alguma coisa e finaliza com .=txt
padrao = re.compile(r'^PGP\w{3,7}_\d{8}-.*\.txt$')

class Arquivo:
    __slots__ = ['_caminho', '_pasta_log', '_data_pasta']

    def __init__(self, caminho=None, pasta_log=None, data_pasta=None):
        self._caminho = caminho
        self._pasta_log = pasta_log
        self._data_pasta = data_pasta

    def pasta_destino(self):
        DATA_ATUAL = self._data_pasta
        MES_ATUAL = datetime.strptime(self._data_pasta, '%d.%m.%Y')
        MES_ATUAL = MES_ATUAL.strftime('%B').upper()
        ANO_ATUAL = datetime.strptime(self._data_pasta, '%d.%m.%Y')
        ANO_ATUAL = ANO_ATUAL.strftime('%Y')

        try:
            if not os.path.exists(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}'):
                os.makedirs(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}')
                os.makedirs(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}/{DATA_ATUAL}')

            if os.path.exists(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}'):
                if not os.path.exists(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}/{DATA_ATUAL}'):
                    os.makedirs(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}/{DATA_ATUAL}')

            if os.path.exists(f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}/{DATA_ATUAL}'):
                return f'{self._caminho}/{MES_ATUAL}-{ANO_ATUAL}/{DATA_ATUAL}/'


        except FileExistsError as error:
            print(f'Nao foi possivel criar a pasta. Erro: {error}')
            return 'ERRO'

    def trata_arquivo(self):
        arq_nome_serializado = self._caminho.split('/')
        caminho_pasta_raiz = os.path.join(*arq_nome_serializado[:-1])
        caminho_pasta_raiz = caminho_pasta_raiz.replace('home', '/home')
        arq_tipo_serializado = arq_nome_serializado[-1].split('_')
        tipo_pgp = arq_tipo_serializado[0][3:]

        rename_arq = arq_tipo_serializado[1].replace('-', '_')

        data_bruta = rename_arq.split('_')
        data_convertida = datetime.strptime(data_bruta[0], '%Y%m%d')
        data_pasta_correta = data_convertida.strftime('%d.%m.%Y')
        self._data_pasta = data_pasta_correta

        if tipo_pgp == 'DHCP':
            pasta_pgp = 'log_DHCP'
        elif tipo_pgp == 'DNS':
            pasta_pgp = 'log_DNS'
        elif tipo_pgp == 'LDAP':
            pasta_pgp = 'log_LDAP'
        elif tipo_pgp == 'PRIMARY':
            pasta_pgp = 'log_PRI'

        # primeiramente tentamos criar a pasta que guardará os logs
        self._caminho = os.path.join(caminho_pasta_raiz, PASTA_LOG, pasta_pgp)
        criacao_pasta = self.pasta_destino()
        if not criacao_pasta == 'ERRO':
            print(f'PASTA {criacao_pasta} existe. Iremos mover os arquivos de PGP pra ela.')
            print('')
            shutil.move(os.path.join(caminho, arq_nome_serializado[-1]), os.path.join(criacao_pasta, rename_arq))
        else:
            print('')
            print(f'Erro na criação da pasta de destino dos arquivos. Verifique os parametros passados.')
            sys.exit()


class MonitorManipulador(PatternMatchingEventHandler):

    def on_modified(self, event):
        #erro de [Errno 2] No such file or directory em centOS no treading. Forca ele a copiar arquivo
        try:
            if os.path.getsize(event.src_path) > 0:
                print(f'Arquivo modificado: {event.src_path}. Tamanho: {os.path.getsize(event.src_path)}')
                arq = Arquivo(event.src_path)
                arq.trata_arquivo()
        except Exception as e:
            print(e)
        finally:
            pass


if __name__ == "__main__":
    event_handler = MonitorManipulador(ignore_directories=True)
    observer = Observer()
    observer.schedule(event_handler, caminho, recursive=False)
    observer.start()

    # aqui procura so na raiz, caso o script tenha parado ele redireciona pras pastas corretas
    for arquivo in os.listdir(caminho):
        if os.path.isfile(os.path.join(caminho, arquivo)) and padrao.match(arquivo):
            lista_arquivos.append(os.path.join(caminho, arquivo))

    print(len(lista_arquivos))
    print(lista_arquivos)

    for caminho_arquivo in lista_arquivos:
        if os.path.getsize(caminho_arquivo) > 0:
            arq = Arquivo(caminho_arquivo)
            arq.trata_arquivo()

    #COMEÇANDO A MONITORAR A PASTA
    print('WATCHDOG TRABALHANDO...')
    print('\n')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
