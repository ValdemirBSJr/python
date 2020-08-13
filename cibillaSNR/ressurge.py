#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#imports
import subprocess
from subprocess import call

get_cibilla_status = subprocess.getoutput('pgrep -fl cibilla.py')

if len(get_cibilla_status) == 0:
    print('Cibilla offline. será iniciado agora..:')
    code_init = call('/home/user/Documentos/SCRIPTS/cibillaSNR/cibilla.py')
    #code_init = call('/home/user/Documentos/SCRIPTS/cibillaSNR/ressucita_cibilla.sh')


else:
    print('cibilla está rodando!')
    print('Processo: {}'.format(get_cibilla_status))
