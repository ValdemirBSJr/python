#!/bin/bash

# Titulo do app
echo -ne "\033]0;Automatizador de Posts - Executor\007"

# --- Encontra o diretório do script ---
# 'realpath "$0"' encontra o caminho completo do script
# 'dirname' pega apenas o diretório
BASE_DIR=$(dirname "$(realpath "$0")")
cd "$BASE_DIR"

# --- Monta o caminho para o script run.py ---
SCRIPT_RUN="$BASE_DIR/run.py"

# --- Execução ---
echo ""
echo "Iniciando o script de configuracao e execucao (run.py)..."
echo "Este script ira criar o 'venv' (se necessario) e instalar as dependencias."
echo "Aguarde ..."
echo ""

# Tenta executar o 'run.py' usando 'python3' (preferencial)
if command -v python3 &> /dev/null; then
    python3 "$SCRIPT_RUN"
# Se 'python3' falhar, tenta 'python'
elif command -v python &> /dev/null; then
    python "$SCRIPT_RUN"
else
    echo "ERRO: Nao foi possivel encontrar 'python3' ou 'python' no seu PATH."
    exit 1
fi

# --- Finalização ---
echo ""
echo "----------------------------------------------------"
echo "Execucao do script finalizada."
echo "Pressione ENTER para fechar esta janela..."
echo "----------------------------------------------------"
read