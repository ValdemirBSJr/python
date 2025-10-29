#! /home/PGP_SRV/venv/bin/python

import verifica_pgp_svd

# pegar o caminho esperado dos servidores que estao listados no controle
caminho_completo_arquivos_esperados = [
        f'{verifica_pgp_svd.caminho}log_{valor["SERVICO"]}/{verifica_pgp_svd.pasta_mes}/{verifica_pgp_svd.pasta_dia}/{verifica_pgp_svd.data_arquivo}_{chave}.txt'
        for chave, valor in verifica_pgp_svd.servidores.items()]

# Listar todos os arquivos existentes nas pastas de PGP e obter o caminho completo
caminho_completo_arquivos_presentes = [verifica_pgp_svd.os.path.join(pasta, arquivo)
                                           for pasta in verifica_pgp_svd.pastas_pgp
                                           for arquivo in verifica_pgp_svd.os.listdir(pasta)
                                           if verifica_pgp_svd.os.path.isfile(verifica_pgp_svd.os.path.join(pasta, arquivo))]

faltantes = verifica_pgp_svd.verificar_arquivos_presentes(caminho_completo_arquivos_presentes, caminho_completo_arquivos_esperados)

ofensores = verifica_pgp_svd.verificar_arquivos_aderentes(caminho_completo_arquivos_presentes, verifica_pgp_svd.padrao_nao_aderente)

print(f'FALTANTES: {faltantes}')

for ofensor in ofensores:
    print(ofensor) 

print(f'QTDE DE ESPERADOS: {len(caminho_completo_arquivos_esperados)}')
print(f'QTDE DE PRESENTES: {len(caminho_completo_arquivos_presentes)}')

