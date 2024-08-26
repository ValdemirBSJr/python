#!/bin/bash

export LANG=en_US.UTF-8

CAMINHO="/home/PGP_SRV/"
CAMINHO_LOG="/home/erros_crontab"
ARQUIVO_LOG="log_ERRO-PGP_SRV.txt"

cd $CAMINHO
$CAMINHO/venv/bin/python verifica_pgp_svd.py 2> $CAMINHO_LOG/$ARQUIVO_LOG

