# Sincronizador LDAP para Proxy de Autenticação

## Visão Geral

Este projeto consiste em um script Python projetado para sincronizar dados de usuários de múltiplos servidores LDAP de origem (e.g., sistemas Solaris ou outros diretórios) para um servidor LDAP local. O principal objetivo é estabelecer o servidor LDAP local como um **proxy de autenticação**. Isso permite que aplicações como o **Semaphore UI** autentiquem usuários de forma centralizada e isolada, sem a necessidade de manter conexões diretas ou replicar todas as complexidades dos servidores LDAP de origem.

O script foca em coletar apenas os atributos essenciais dos usuários e replicá-los no servidor de destino, garantindo uma estrutura de usuário limpa e padronizada (geralmente baseada em `inetOrgPerson`), facilitando a gestão e compatibilidade com aplicações que consomem o diretório local.

## Funcionalidades Principais

* **Coleta de Usuários Flexível:** Conecta-se a uma lista configurável de servidores LDAP de origem para coletar informações de usuários.
* **Filtragem de Atributos:** Permite definir quais atributos específicos (`uid`, `cn`, `mail`, `userPassword`, etc.) devem ser copiados da origem para o destino.
* **Sincronização Inteligente:**
    * **Criação:** Adiciona novos usuários que existem na origem, mas ainda não no servidor LDAP de destino.
    * **Atualização:** Modifica atributos de usuários já existentes no destino, garantindo que estejam atualizados com os dados da origem.
* **Estrutura Limpa:** Cria entradas de usuários no destino com `objectClass` padrão (`top`, `person`, `organizationalPerson`, `inetOrgPerson`), ignorando complexidades ou `objectClass` específicas do ambiente de origem.
* **Gerenciamento de Dependências com `uv`:** Utiliza o `uv` para criar e gerenciar um ambiente virtual isolado e instalar as dependências do projeto de forma eficiente.
* **Configuração Segura:** Carrega todas as credenciais e parâmetros sensíveis a partir de um arquivo `.env`, protegendo informações confidenciais de serem versionadas.
* **Logging Detalhado:** Emprega o módulo `logging` do Python para fornecer feedback claro e estruturado sobre o progresso da sincronização e quaisquer erros encontrados.

## Estrutura do Projeto

.
├── .env                  # Arquivo de variáveis de ambiente (credenciais, URLs)
├── config.py             # Módulo Python para carregar e validar as configurações do .env.
├── sincronizador.py      # Script principal contendo a lógica de coleta e sincronização LDAP.
├── requirements.txt      # Lista de dependências Python para o 'uv'.
├── .gitignore            # Define quais arquivos/pastas o Git deve ignorar.
└── README.md             # Este arquivo, com informações sobre o projeto.


## Pré-requisitos

* **Python 3.8+**: Certifique-se de ter uma versão compatível do Python instalada.
* **`uv`**: O gerenciador de pacotes e ambientes virtuais (substituto de `pip` e `venv`). Instale-o seguindo as instruções oficiais do `uv`.
* **Servidores LDAP de Origem**: Acesso a um ou mais servidores LDAP que contenham os usuários a serem sincronizados, com credenciais de leitura válidas.
* **Servidor LDAP de Destino**: Um servidor LDAP (e.g., OpenLDAP/slapd) configurado e rodando localmente (ou em um host acessível), com credenciais de administrador que possuam permissões para adicionar e modificar entradas de usuários na `BASE_DN_DESTINO` configurada (no exemplo estou implementando na máquina local).
* **Ferramentas LDAP no Sistema Operacional**: `slapd`, `ldap-utils`, `slapd-contrib` para o servidor LDAP local.

* **Crie um arquivo chamado .env na raiz do seu projeto.**:

# Se houver múltiplos servidores, separe-os por vírgula, sem espaços.
SERVIDORES_ORIGEM="10.0.0.1,10.0.0.2
USUARIO_ORIGEM="CN=proxyagent,DC=dcExample"
SENHA_ORIGEM="origin_passwd"
BASE_DN_ORIGEM="ou=people,dc=user,dc=group"
FILTRO_BUSCA_ORIGEM="(&(objectClass=posixAccount)(uid=*))" # Filtro LDAP para buscar usuários

# --- Configuração do Servidor de Destino (seu slapd local ou outro LDAP proxy) ---
URI_SERVIDOR_DESTINO="ldap://localhost:389" # Endereço do seu servidor LDAP de destino
USUARIO_ADMIN_DESTINO="cn=admin,dc=user,dc=group"
SENHA_ADMIN_DESTINO="pass_slapd" # Senha do usuário administrador do LDAP de destino
BASE_DN_DESTINO="dc=user,dc=group" # Base DN onde os usuários serão criados/atualizados no destino

# --- Atributos a serem copiados da origem para o destino ---
# Liste os atributos desejados, separados por vírgula, sem espaços.
ATRIBUTOS_PARA_COPIAR="uid,cn,sn,givenName,mail,userPassword,displayName"

# Instala o servidor OpenLDAP e utilitários
sudo apt update
sudo apt install slapd ldap-utils slapd-contrib python3-ldap3 -y

# /etc/ldap/slapd.conf

# Arquivo de Configuração do Slapd - Modo Agregador com SyncRepl (Adaptação para Proxy Local)
#=======================================================================
# Incluir schemas básicos
include /etc/ldap/schema/core.schema
include /etc/ldap/schema/cosine.schema
include /etc/ldap/schema/inetorgperson.schema
include /etc/ldap/schema/nis.schema
 
# Módulos e configuração básica
modulepath /usr/lib/ldap/
moduleload back_mdb.so # Ou back_hdb.so, dependendo da sua preferência
pidfile /var/run/slapd/slapd.pid
argsfile /var/run/slapd/slapd.args
loglevel 256 # Ajuste o nível de log conforme necessário para depuração
 
#=======================================================================
# DEFINIÇÃO DO BANCO DE DADOS LOCAL
#=======================================================================
database mdb
# O sufixo (Base DN) do nosso novo servidor local unificado
suffix "dc=user,dc=group"
# O diretório onde os dados serão armazenados
directory /var/lib/ldap
# O usuário administrador deste servidor local (a senha é definida com ldappasswd ou no LDIF)
rootdn "cn=admin,dc=user,dc=group"
rootpw {SSHA}HASH_DA_SENHA # **Substitua por um hash SSHA real da sua senha**
# Alternativamente, a senha pode ser definida no arquivo LDIF de inicialização, como no seu exemplo.
# Para gerar um hash SSHA de 'pass_slapd':
# echo -n "pass_slapd" | slappasswd -s "" -h {SSHA}
# Copie a saída para 'rootpw'.

# Indexação para buscas rápidas
index objectClass eq
index uid eq
index cn eq
index mail eq
index sn eq

# /root/init.ldif
dn: dc=user,dc=group
objectClass: top
objectClass: dcObject
objectclass: organization
o: Semaphore Users
 
dn: cn=admin,dc=user,dc=group
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
userPassword: pass_slapd # **Substitua pela sua senha real**

* **Cria o ambiente virtual e instala todas as dependências**:
`uv sync`

# Cria o ambiente virtual (geralmente em ./.venv) e instala todas as dependências
uv sync

