# Zabbix Alert Enricher with AI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Redis](https://img.shields.io/badge/Redis-red?style=for-the-badge&logo=redis)
![Zabbix](https://img.shields.io/badge/Zabbix-darkblue?style=for-the-badge&logo=zabbix)

## 📖 Visão Geral

Este projeto consiste em um script Python projetado para ser integrado ao Zabbix como um script de alerta (AlertScript). Seu principal objetivo é enriquecer os alertas gerados pelo Zabbix com análises e sugestões de troubleshooting geradas por Inteligência Artificial através da API da [Groq](https://groq.com/).

O script utiliza o Redis para manter um histórico de alertas recorrentes. Ao receber um novo alerta, ele verifica se um problema semelhante já ocorreu e utiliza essa informação como contexto adicional para a IA, permitindo que a sugestão gerada seja mais precisa e refinada ao longo do tempo.


## ✨ Funcionalidades

- **Integração com Zabbix:** Recebe informações de alertas diretamente dos parâmetros do Zabbix.
- **Análise por IA:** Envia os detalhes do alerta para a API da Groq para obter uma análise técnica e sugestões de troubleshooting.
- **Contexto Histórico com Redis:** Armazena um histórico de alertas para refinar futuras análises da IA, aprendendo com ocorrências passadas.
- **Design Modular:** Utiliza o padrão Pipeline para separar claramente as responsabilidades: buscar histórico, montar prompt, consultar a IA e persistir resultados.
- **Configuração Flexível:** Utiliza um arquivo `.env` para gerenciar chaves de API e configurações de conexão, mantendo os segredos fora do código.
- **Segurança:** Os paramêtros passados ao groq não incluem informação sensível sobre ip e hostname dos equipamentos. Para uma análise mais profunda com esses parâmetros, sugiro um modelo self-hosted.

## 🛠️ Configuração e Instalação

Siga os passos abaixo para configurar e executar o script no seu ambiente.

### 1. Pré-requisitos

- Python 3.8 ou superior
- **[uv](https://github.com/astral-sh/uv)** (um instalador e gerenciador de ambientes Python extremamente rápido)
- Acesso a um servidor Redis
- Uma conta e chave de API da [Groq](https://console.groq.com/keys)
- Um servidor Zabbix configurado para usar AlertScripts.

### 2. Instale as Dependências com `uv`

```bash
# 1. Crie um ambiente virtual usando uv (ele criará uma pasta .venv por padrão)
uv venv

# 2. Ative o ambiente virtual
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# 3. Instale as dependências definidas no pyproject.toml e uv.lock
uv sync
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes informações:

```ini
# Chave de API obtida no painel da Groq
GROQ_API_KEY="gsk_sua_chave_secreta_aqui"

# Configurações do seu servidor Redis
REDIS_HOST="localhost"
REDIS_PORT="6379"
```

### Integração com o Zabbix

1.  **Copie o script** para o diretório de AlertScripts do seu servidor Zabbix (geralmente `/usr/lib/zabbix/alertscripts/`).
2.  **Crie o arquivo `.env`** para o mesmo diretório para que o script possa carregar as configurações.
3.  **Configure um novo "Alerta"** no Zabbix do tipo "Script".
4.  **Adicione os parâmetros** necessários ao script na configuração do alerta. A ordem é importante:
    - `{TRIGGER.HOSTGROUP.NAME}`
    - `{TRIGGER.DESCRIPTION}`
    - `{TRIGGER.EXPRESSION}`
    - `{TRIGGER.RECOVERY.EXPRESSION}`
5.  **Crie o apontamento do script no alerta:** /usr/lib/zabbix/alertscripts/main_zabbix_grok.py "{TRIGGER.DESCRIPTION}" "{TRIGGER.HOSTGROUP.NAME}" "{TRIGGER.EXPRESSION}" "{TRIGGER.EXPRESSION.RECOVERY}".
