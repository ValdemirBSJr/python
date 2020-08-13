#!/bin/bash

if pgrep -fl cibilla.py
  then
  # RODANDO
  echo "Rodando!"
  else
  #NÃO TA RODANDO
  echo "Não tá rodando!"
  echo "Rodando agora...(|/)"
  /home/user/.virtualenvs/k36/bin/python   /home/user/Documentos/SCRIPTS/cibillaSNR/cibilla.py
fi


