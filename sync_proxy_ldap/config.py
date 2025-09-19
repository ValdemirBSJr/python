"""
Módulo para carregar e validar as configurações a partir do arquivo .env.
"""
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração dos Servidores de Origem ---
# Converte a string de servidores separada por vírgula em uma lista
SERVIDORES_ORIGEM = os.getenv("SERVIDORES_ORIGEM", "").split(',')
USUARIO_ORIGEM = os.getenv("USUARIO_ORIGEM")
SENHA_ORIGEM = os.getenv("SENHA_ORIGEM")
BASE_DN_ORIGEM = os.getenv("BASE_DN_ORIGEM")
FILTRO_BUSCA_ORIGEM = os.getenv("FILTRO_BUSCA_ORIGEM")

# --- Configuração do Servidor de Destino ---
URI_SERVIDOR_DESTINO = os.getenv("URI_SERVIDOR_DESTINO")
USUARIO_ADMIN_DESTINO = os.getenv("USUARIO_ADMIN_DESTINO")
SENHA_ADMIN_DESTINO = os.getenv("SENHA_ADMIN_DESTINO")
BASE_DN_DESTINO = os.getenv("BASE_DN_DESTINO")

# --- Atributos a serem copiados ---
# Converte a string de atributos separada por vírgula em uma lista
ATRIBUTOS_PARA_COPIAR = os.getenv("ATRIBUTOS_PARA_COPIAR", "").split(',')

# Validação simples para garantir que variáveis essenciais foram carregadas
if not all([SERVIDORES_ORIGEM, USUARIO_ORIGEM, SENHA_ORIGEM, BASE_DN_ORIGEM, URI_SERVIDOR_DESTINO, USUARIO_ADMIN_DESTINO, SENHA_ADMIN_DESTINO, BASE_DN_DESTINO, ATRIBUTOS_PARA_COPIAR]):
    raise ValueError("Uma ou mais variáveis de ambiente essenciais não foram definidas no arquivo .env.")
