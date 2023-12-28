from pathlib import Path
import os
import requests
import tarfile
from datetime import datetime

URL = r'https://seusite.dominio.com.br/backup/'
DIRETORIO = Path(__file__).resolve().parent
LISTA_OLT = [

'192.168.0.1',
'192.168.0.2',
'192.168.0.3',
'192.168.0.4',
'192.168.0.5',

]

DATA_ATUAL_CAMINHO = datetime.now().strftime('%d.%m.%Y')

def verifica_pagina(url: str) -> bool:
    '''

    :param url: caminho da pagina  de download
    :return: booleano True para esta ok e False para erro
    '''
    try:
        #verify=false pois o certificado ssl do repositorio ta vencido kkk
        resposta = requests.get(url, verify=False)
        resposta.raise_for_status()

        if resposta.status_code == 200:
            return True
        else:
            raise Exception(f'Recebemos um codigo diferente do acesso permitido. Codigo: {resposta.status_code}.')
            return False

    except requests.exceptions.RequestException as e:
        print(f'URL nao esta acessivel. Verifique se o endereco esta correto e/ou se tem pemissao pra visualizacao da pagina: {url}. Erro: {e}')
        return False

def baixa_tar(url: str):
    '''
    verifica com a funcao verifica_pagina se a pagina de download esta acessível
    depois faz o download do arquivo diario
    :param url: link da pagina
    :return: True para teve sucesso em baixar e False para houve erro
    '''
    if verifica_pagina(url):
        baixa_arquivo = requests.get(url + 'backup.tar.gz', verify=False)
        with open('backup.tar.gz', 'wb') as gzip_baixado:
            gzip_baixado.write(baixa_arquivo.content)
            return True
    else:
        raise Exception('Nao foi possivel baixar o arquivo backup.tar.gz')
        return False

def descompacta_gzip(nome_arquivo: str):
    '''
    funcao de teste nao usado em producao. Apenas para descompactar o gzip baixado.
    :param nome_arquivo: nome do arquivo gzip baixado do dia
    '''
    with tarfile.open(str(DIRETORIO / nome_arquivo), 'r:gz') as gzip_entrada:
        #descompacta tudo obedecendo a hierarquia das pastas
        gzip_entrada.extractall()

def le_gzip(nome_arquivo: str):
    '''
    funcao de teste nao usado em producao. Apenas para ler o arquivo.
    :param nome_arquivo: nome do arquivo gzip baixado do dia
    '''
    with tarfile.open(str(DIRETORIO / nome_arquivo), 'r:gz') as gzip_entrada:
        #percorre o defaultdict gerado e descreve item a item, primeiro a pasta depois sub e por ai vai ate arquivo final
        for tar_info in gzip_entrada:
            print(f'{tar_info.name} tem {tar_info.size} bytes de tamanho.')
            if tar_info.isfile():
                print(f'{tar_info} é um arquivo valido')
            elif tar_info.isdir():
                print(f'{tar_info} é um diretorio')
            else:
                print(f'{tar_info} é outra coisa')

def filtra_olts(nome_arquivo: str, lista_olts: list):
    '''
    funcao que verifica se o arquivo foi baixado e abre o tar.gz e cria um novo arquivo
    apenas com as pastas e arquivos
    que contem na lista de OLT da nossa base.
    :param nome_arquivo: nome do arquivo tar.gz baixado no dia
    :param lista_olts: lista de OLT que iremos salvar no arquivo final
    '''
    # acrescento o caminho completo para referencia dos membros da lista
    #lista_olts = [str(r'home/ftpdir/' + olt) for olt in lista_olts]
    print('VAMOS COLETAR OS BKP...', end='\n\n')
    print('Tentando aceder ao site...', end='\n\n')
    if baixa_tar(URL):
        with tarfile.open(str(DIRETORIO / nome_arquivo), 'r:gz') as gzip_entrada:
            # salva todos os membros de um arquivo, pastas e subs e arquivos
            membros = gzip_entrada.getmembers()
            print('Arquivo coletado!', end='\n\n')

            # agora vamos filtras os membros de acordo com a lista de olts que queremos manter
            membros_filtrados = [membro for membro in membros if any(pasta in membro.name for pasta in lista_olts)]
            print('Filtrando os membros do nosso cluster...', end='\n\n')

            # criamos um novo arquivo tar.gz apenas com os membros que queremos
            with tarfile.open(str(DIRETORIO / f'backup_{DATA_ATUAL_CAMINHO}.tar.gz'), 'w:gz') as gzip_saida:
                for membro in membros_filtrados:
                    gzip_saida.addfile(membro, gzip_entrada.extractfile(membro))

            print('Salvando o novo arquivo com os membros requeridos...', end='\n\n')
            #fecha e apaga arquivo antigo com todos os membros do BR
            gzip_entrada.close()
            os.remove(str(DIRETORIO / nome_arquivo))

            #move para a pasta final
            os.rename(str(DIRETORIO / f'backup_{DATA_ATUAL_CAMINHO}.tar.gz'), str(DIRETORIO / f'BKP/backup_{DATA_ATUAL_CAMINHO}.tar.gz'))
            print('SCRIPT FINALIZADO!!!!')





if __name__ == '__main__':
    filtra_olts(str(DIRETORIO / 'backup.tar.gz'), LISTA_OLT)
    #print(verifica_pagina(URL))



