# Sincronizador LDAP para Proxy de Autenticação

## Visão Geral

Este projeto consiste em um script Python projetado para sincronizar dados de usuários de múltiplos servidores LDAP de origem (por exemplo, sistemas Solaris ou outros diretórios) para um servidor LDAP local. O principal objetivo é estabelecer o servidor LDAP local como um **proxy de autenticação**.

Isso permite que aplicações como o **Semaphore UI** autentiquem usuários de forma centralizada e isolada, sem a necessidade de manter conexões diretas ou replicar todas as complexidades dos servidores LDAP de origem.

O script foca em coletar apenas os atributos essenciais dos usuários e replicá-los no servidor de destino, garantindo uma estrutura de usuário limpa e padronizada (geralmente baseada em `inetOrgPerson`), facilitando a gestão e compatibilidade com aplicações que consomem o diretório local.

---

## Funcionalidades Principais

- **Coleta de Usuários Flexível**: Conecta-se a uma lista configurável de servidores LDAP de origem para coletar informações de usuários.
- **Filtragem de Atributos**: Permite definir quais atributos específicos (`uid`, `cn`, `mail`, `userPassword`, etc.) devem ser copiados da origem para o destino.
- **Sincronização Inteligente**:
  - **Criação**: Adiciona novos usuários que existem na origem, mas ainda não no servidor LDAP de destino.
  - **Atualização**: Modifica atributos de usuários já existentes no destino, garantindo que estejam atualizados com os dados da origem.
- **Estrutura Limpa**: Cria entradas de usuários no destino com `objectClass` padrão (`top`, `person`, `organizationalPerson`, `inetOrgPerson`), ignorando complexidades ou `objectClass` específicas do ambiente de origem.
- **Gerenciamento de Dependências com `uv`**: Utiliza o `uv` para criar e gerenciar um ambiente virtual isolado e instalar as dependências do projeto de forma eficiente.
- **Configuração Segura**: Carrega todas as credenciais e parâmetros sensíveis a partir de um arquivo `.env`, protegendo informações confidenciais de serem versionadas.
- **Logging Detalhado**: Emprega o módulo `logging` do Python para fornecer feedback claro e estruturado sobre o progresso da sincronização e quaisquer erros encontrados.

---

## Estrutura do Projeto

```bash
.
├── .env
├── config.py
├── sincronizador.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Pré-requisitos

- **Python 3.8+**: Certifique-se de ter uma versão compatível do Python instalada.
- **`uv`**: Gerenciador de pacotes e ambientes virtuais (substituto de `pip` e `venv`). Instale seguindo as [instruções oficiais do `uv`](https://github.com/astral-sh/uv).
- **Servidores LDAP de Origem**: Acesso a um ou mais servidores LDAP contendo os usuários a serem sincronizados, com credenciais de leitura válidas.
- **Servidor LDAP de Destino**: Um servidor LDAP (por exemplo, OpenLDAP/slapd) configurado e rodando localmente (ou em host acessível), com credenciais de administrador que possuam permissões para adicionar e modificar entradas de usuários na `BASE_DN_DESTINO` configurada.
- **Ferramentas LDAP no Sistema Operacional**: Pacotes como `slapd`, `ldap-utils` e `slapd-contrib` devem estar instalados.

---

## Configuração Inicial

### 1. Instalação do OpenLDAP e Dependências

```bash
sudo apt update
sudo apt install slapd ldap-utils slapd-contrib python3-ldap3 -y

# Incluir schemas básicos
include /etc/ldap/schema/core.schema
include /etc/ldap/schema/cosine.schema
include /etc/ldap/schema/inetorgperson.schema
include /etc/ldap/schema/nis.schema

# Módulos e configuração básica
modulepath /usr/lib/ldap/
moduleload back_mdb.so
pidfile /var/run/slapd/slapd.pid
argsfile /var/run/slapd/slapd.args
loglevel 256
```

# DEFINIÇÃO DO BANCO DE DADOS LOCAL

```bash
database mdb
suffix "dc=user,dc=group"
directory /var/lib/ldap
rootdn "cn=admin,dc=user,dc=group"
rootpw {SSHA}HASH_DA_SENHA

# Indexação para buscas rápidas
index objectClass eq
index uid eq
index cn eq
index mail eq
index sn eq
```

## Para gerar o hash SSHA da senha:
```bash
slappasswd -s "pass_slapd" -h {SSHA}
```

## Copie a saída para 'rootpw'.

## Inicialização da Base LDAP:
## /root/init.ldif
```bash
dn: dc=user,dc=group
objectClass: top
objectClass: dcObject
objectClass: organization
o: Semaphore Users

dn: cn=admin,dc=user,dc=group
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
userPassword: pass_slapd
```

## Carregamento do LDIF:

```bash
ldapadd -x -D "cn=admin,dc=user,dc=group" -W -f init.ldif
```

## Arquivo .env:

```bash
SERVIDORES_ORIGEM="10.0.0.1,10.0.0.2"
USUARIO_ORIGEM="CN=proxyagent,DC=dcExample"
SENHA_ORIGEM="origin_passwd"
BASE_DN_ORIGEM="ou=people,dc=user,dc=group"
FILTRO_BUSCA_ORIGEM="(&(objectClass=posixAccount)(uid=*))"


URI_SERVIDOR_DESTINO="ldap://localhost:389"
USUARIO_ADMIN_DESTINO="cn=admin,dc=user,dc=group"
SENHA_ADMIN_DESTINO="pass_slapd"
BASE_DN_DESTINO="dc=user,dc=group"


ATRIBUTOS_PARA_COPIAR="uid,cn,sn,givenName,mail,userPassword,displayName"
```

# Cria o ambiente virtual e instala todas as dependências:
`uv sync`

# Cria o ambiente virtual (geralmente em ./.venv) e instala todas as dependências
`uv sync`


