#! /home/PGP_SRV/venv/bin/python
import os
import subprocess
from Servidores import servidores
from datetime import datetime

# Configuracoes
pasta_bot_tg = '/home/'
caminho = '/home/PGP_SRV/'
data_atual = datetime.now()
pasta_mes = data_atual.strftime('%B-%Y').upper()
pasta_dia = data_atual.strftime('%d.%m.%Y')
data_arquivo = data_atual.strftime('%Y%m%d')
pastas_pgp = [f'{caminho}log_DHCP/{pasta_mes}/{pasta_dia}/', f'{caminho}log_DNS/{pasta_mes}/{pasta_dia}/', f'{caminho}log_LDAP/{pasta_mes}/{pasta_dia}/', f'{caminho}log_PRI/{pasta_mes}/{pasta_dia}/']
padrao_nao_aderente = r'NOK'
assunto = f'Certifica&#231;&#227;o PGP SERVIDORES - {data_atual.strftime("%d/%m/%Y")}'
resumo = ''

# Funcao para verificar se todos os arquivos necessarios estao presentes
def verificar_arquivos_presentes(arquivos_presentes, arquivos_esperados):
    arquivos_faltando = [arquivo for arquivo in arquivos_esperados if arquivo not in arquivos_presentes]
    # separa cada um por /
    faltantes_splitados = [faltante.split('/') for faltante in arquivos_faltando]
    # pega o tipo de log na 7 posicao e o nome do arquivo na 10 e monta a string
    faltantes_formatados = [str(faltante[4][4:] + '->' + faltante[7][9:-4]) for faltante in faltantes_splitados]

    return faltantes_formatados

# Funcao para verificar o conteudo dos arquivos. se ta aderente
def verificar_arquivos_aderentes(caminhos_arquivos_presentes, criterio):
    linhas_ofensoras = []
    for arquivo in caminhos_arquivos_presentes:
        with open(arquivo, 'r', encoding='utf-8') as arq:
            for linha in arq:
                if criterio in linha:
                    linhas_ofensoras.append(linha)
    return linhas_ofensoras



if __name__ == "__main__":
    # pegar o caminho esperado dos servidores que estao listados no controle
    caminho_completo_arquivos_esperados = [
        f'{caminho}log_{valor["SERVICO"]}/{pasta_mes}/{pasta_dia}/{data_arquivo}_{chave}.txt'
        for chave, valor in servidores.items()]

    # Listar todos os arquivos existentes nas pastas de PGP e obter o caminho completo
    caminho_completo_arquivos_presentes = [os.path.join(pasta, arquivo)
                                           for pasta in pastas_pgp
                                           for arquivo in os.listdir(pasta)
                                           if os.path.isfile(os.path.join(pasta, arquivo))]

    faltantes = verificar_arquivos_presentes(caminho_completo_arquivos_presentes, caminho_completo_arquivos_esperados)

    ofensores = verificar_arquivos_aderentes(caminho_completo_arquivos_presentes, padrao_nao_aderente)

    print(f'FALTANTES: {faltantes}')
    print(f'OFENSORES: {ofensores}')
    print(f'QTDE DE ESPERADOS: {len(caminho_completo_arquivos_esperados)}')
    print(f'QTDE DE PRESENTES: {len(caminho_completo_arquivos_presentes)}')

    if len(ofensores) > 0:
        resumo += 'SEGUE LISTA DOS ITENS OFENSORES:&#10;'
        for ofensor in ofensores:
            resumo += str(ofensor + '&#10;')  # 96.39
        resumo += '&#10;'
    else:
        resumo += '+++ PGP SEM OFENSORES NO MOMENTO. TUDO ADERENTE! +++&#10;'

    if len(faltantes) > 0:
        resumo += 'EXISTEM SERVIDORES NAO COLETADOS (Favor rodar manual)&#10;'
        for faltante in faltantes:
            resumo += str(faltante + '&#10;')

    comando_bot_tg = f'{pasta_bot_tg}hub_bot_tg.sh {pasta_bot_tg}lista_mailing_tg.txt "{assunto}" "{resumo}" {pasta_bot_tg}erros_crontab/log_ERRO-PGP_SRV.txt'
    comando_aplicado_tg = subprocess.run(comando_bot_tg, shell=True, capture_output=True)
    retorno_comando_tg = comando_aplicado_tg.returncode

    if retorno_comando_tg == 0:
        print('Mensagem do telegram enviada com SUCESSO!')
    else:
        print('OCORREU UM ERRO AO ENVIAR A MENSAGEM VIA BOT!')


