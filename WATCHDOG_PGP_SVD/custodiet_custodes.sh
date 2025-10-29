#!/bin/bash

if pgrep -fl monitor_pgp.py
  then
  # RODANDO
  echo " Monitor rodando!"
  # Agora verifica se tem duplicata
  CONTA_PROCESSOS=$(pgrep -f monitor_pgp.py | wc -l)
  if [ $CONTA_PROCESSOS -gt 1 ]; then
    echo "Mais de uma instância do script está rodando. Matando processos duplicados..."
    pgrep -f monitor_pgp.py | tail -n +2 | xargs kill -9
else
    echo "Nenhuma duplicata encontrada. O script está rodando normalmente."
fi
  else
  #NÃO TA RODANDO
  echo "Não tá rodando!"
  echo "Rodando agora...(|/)"
  /home/PGP_SRV/venv/bin/python /home/PGP_SRV/monitor_pgp.py 2> /home/erros_crontab/log_CUSTODIET_pgp.txt
fi
