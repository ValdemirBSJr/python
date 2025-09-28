# 🤖 IA de Pergunta e Resposta Customizável

### Treine uma Inteligência Artificial para ser especialista nos seus próprios documentos

![Python](https://img.shields.io/badge/Python-3.9%2B-blueviolet.svg)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Transformers-yellow.svg)

Este projeto apresenta um pipeline completo para transformar uma coleção de documentos (`.pdf`, `.docx`, `.txt`) em uma base de conhecimento interativa, alimentada por um modelo de linguagem (LLM) ajustado (fine-tuned) especificamente para responder perguntas sobre o conteúdo desses documentos.

---

## 📜 Índice

* [Sobre o Projeto](#-sobre-o-projeto)
* [✨ Funcionalidades](#-funcionalidades)
* [🛠️ Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [🚀 Começando](#-começando)
    * [Pré-requisitos](#pré-requisitos)
    * [Instalação](#instalação)
* [▶️ Como Usar](#-como-usar)
* [📂 Estrutura do Projeto](#-estrutura-do-projeto)

---

## 📖 Sobre o Projeto

A informação em empresas e projetos pessoais muitas vezes fica presa dentro de documentos não estruturados. Encontrar uma resposta específica pode ser um processo manual e demorado.

Este projeto resolve esse problema através da criação de um modelo de **Pergunta e Resposta (Question Answering - QA)** customizado. O fluxo de trabalho é o seguinte:

1.  **Extração de Texto:** O sistema lê automaticamente o conteúdo de todos os arquivos na pasta `arquivos_base`.
2.  **Geração Automática de Dataset:** Utilizando um modelo T5, o script `treinador.py` gera um conjunto de dados sintético com pares de perguntas e respostas relevantes a partir do texto extraído.
3.  **Fine-Tuning:** Um modelo de linguagem pré-treinado da Hugging Face (como o `deepset/roberta-base-squad2`) é então ajustado com este novo dataset, tornando-se um especialista no seu conteúdo.
4.  **Teste Interativo:** Com o script `teste_pipeline.py`, é possível conversar com o modelo treinado, fazendo perguntas em linguagem natural e recebendo respostas precisas baseadas nos documentos fornecidos.

O resultado é uma IA que funciona como um assistente especialista, pronto para responder qualquer pergunta sobre a sua base de conhecimento.

---

## ✨ Funcionalidades

* **Suporte a Múltiplos Formatos:** Extrai texto de arquivos `.pdf`, `.docx` e `.txt`.
* **Dataset Sintético:** Cria automaticamente dados de alta qualidade para o treinamento, eliminando a necessidade de anotação manual.
* **Treinamento Simplificado:** Utiliza a biblioteca `Trainer` da Hugging Face para um processo de fine-tuning robusto e eficiente.
* **Pipeline de Teste:** Inclui um script interativo para validar e utilizar o modelo treinado diretamente pelo terminal.
* **Exportável:** O modelo pode ser facilmente exportado para outros formatos, como ONNX, para otimização e implantação em diferentes ambientes.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.9+**
* **Hugging Face Transformers:** Para acesso a modelos pré-treinados e ao pipeline de treinamento.
* **Hugging Face Datasets:** Para manipulação eficiente dos dados.
* **PyTorch:** Como backend de deep learning.
* **PyPDF2** e **python-docx:** Para extração de texto de arquivos.
* **Optimum:** Para exportação de modelos para o formato ONNX.

---

## 🚀 Começando

Siga estas instruções para ter uma cópia do projeto rodando na sua máquina local.

### Pré-requisitos

Você precisa ter o Python 3.9 (ou superior) e o `pip` instalados.

Crie um arquivo `requirements.txt` na raiz do projeto com o seguinte conteúdo:

```txt
transformers
datasets
torch
PyPDF2
python-docx
sentencepiece
onnx
onnxruntime
optimum
```

## 📂 Estrutura do Projeto

```bash
.
├── arquivos_base/            # ⬅️ Coloque seus documentos aqui
├── meu_modelo_ajustado/      # 📂 Onde o modelo treinado é salvo
├── modelo_onnx/              # 📂 Onde o modelo exportado para ONNX é salvo
├── resultados/               # 📂 Checkpoints e logs do treinamento
│
├── treinador.py              # 📜 Script principal para processar dados e treinar o modelo
├── teste_pipeline.py         # 🤖 Script para interagir com o modelo treinado
├── converter_para_gguf.py    # 📦 Script para conversão do modelo ONNX (passo avançado)
├── pr_dataset.json           # 📄 Dataset de perguntas e respostas gerado automaticamente
├── requirements.txt          # 📄 Lista de dependências do projeto
└── README.md                 # 📄 Arquivo de documentação
```

## 🚀 Instalação com uv

### Estas instruções assumem que você já tem o uv instalado no seu sistema.

- Clone o repositório:

```bash

git clone [https://github.com/ValdemirBSJr/python/tree/master/treinando_IA_modelo_ds](https://github.com/ValdemirBSJr/python/tree/master/treinando_IA_modelo_ds)
```

- Navegue até o diretório do projeto:

```bash
cd seu-repositorio
```

- Crie e ative um ambiente virtual com uv:

```bash
uv venv
```

## Ativa o ambiente

- No Linux ou macOS:

```bash
source .venv/bin/activate
```

- No Windows (CMD):

```bash
.venv\Scripts\activate
```

- Instale as dependências usando uv:

```bash
uv pip install -r requirements.txt

```
