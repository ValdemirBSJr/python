@echo off
REM Define o título da janela do terminal
TITLE Automatizador de Posts - Executor

REM --- Encontra o diretório do script ---
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

REM --- Monta o caminho para o script run.py ---
set "SCRIPT_RUN=%BASE_DIR%run.py"

REM --- Execução ---
echo.
echo Iniciando o script de configuracao e execucao (run.py)...
echo Este script ira criar o 'venv' (se necessario) e instalar as dependencias.
echo Por favor, aguarde...
echo.

REM Tenta executar o 'run.py' usando o 'py' launcher (preferencial no Windows)
py.exe "%SCRIPT_RUN%"

REM Se 'py.exe' falhar (não encontrado), tenta usar 'python.exe'
if %errorlevel% neq 0 (
    echo "py.exe nao encontrado, tentando 'python.exe'..."
    python.exe "%SCRIPT_RUN%"
)

REM --- Finalização ---
echo.
echo ----------------------------------------------------
echo Execucao do script finalizada.
echo Pressione qualquer tecla para fechar esta janela...
echo ----------------------------------------------------
pause > nul