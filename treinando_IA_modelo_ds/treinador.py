#instalar o cmake e caso nao va pro path do win adicionar ele
#pip install PyPDF2 python-docx transformers datasets torch
#pip install transformers[sentencepiece]
#pip install transformers[torch]
#pip install onnx
#pip install onnx onnxruntime
#pip install optimum
#pip install gguf

'''
Ele vai gerar varios arquivos na pasta meu_modelo_ajustado.
Ex:  config.json model.safetensors tokenizer_config.json vocab.txt special_tokens_map.json training_args.bin

Depois do treinamento: vao no terminal do venv:
1 - exporte o modelo para o formato ONNX:
optimum-cli export onnx --model ./meu_modelo_ajustado --task question-answering ./modelo_onnx

2 - converta ONNX para GGUF:
rodar converter_para_gguff.py

3 - rode no ollama:
ollama serve
ollama list
ollama create meu-modelo-teste -f C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\meu-modelo-teste.modelfile
ollama run meu-modelo-teste

O LM studio GGUF ou diretamente no formato do hugging face

RAG ou PROMPT ENGINEERING

'''

import os
import json
import PyPDF2
from docx import Document
from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# Funcao para extrair texto de PDF
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, "rb") as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text()
        return texto

# Funcao para extrair texto de DOCX
def extrair_texto_docx(caminho_docx):
    docx = Document(caminho_docx)
    texto = ""
    for paragrafo in docx.paragraphs:
        texto += paragrafo.text + "\n"
    return texto

# Funcao para extrair texto de TXT
def extrair_texto_txt(caminho_txt):
    with open(caminho_txt, "r", encoding="utf-8") as arquivo:
        return arquivo.read()

# Funcao para gerar perguntas e respostas automaticamente a partir dos textos
def gerar_pr_pares(contexto):
    #nome do modelo ajustado para geracao de perguntas
    nome_modelo_T5 = "valhalla/t5-small-qa-qg-hl"
    # se o idioma bugar use: unicamp-dl/ptt5-base-qa-qg
    # ou pierreguillou/t5-small-pt-br
    tokenizador = T5Tokenizer.from_pretrained(nome_modelo_T5)
    modelo = T5ForConditionalGeneration.from_pretrained(nome_modelo_T5)

    # Pre-processar o texto
    texto_input = f"generate questions in Portuguese: {contexto}"
    #texto_input = f"generate questions: {contexto}"
    inputs = tokenizador(texto_input, return_tensors="pt", max_length=512, truncation=True)

    # Gerar perguntas
    outputs = modelo.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=64, # comprimento maximo da sequencia gerada
        num_return_sequences=3, # Define quantas sequencias de saida serao geradas
        num_beams=5, # Numero de beams(hipoteses) para beam search (deve ser >= num de sequencias desejadas)
        no_repeat_ngram_size=2,  # Evita repeticao de n-grams (ex.: palavras repetidas)
        early_stopping=True,  # Para a geracao assim que a sequencia estiver completa
    )

    # Decodificar as perguntas geradas
    questoes = [tokenizador.decode(output, skip_special_tokens=True) for output in outputs]

    # Criar pares de perguntas e respostas
    pares_perg_resp = []
    for questao in questoes:
        pares_perg_resp.append({
            "context": contexto,
            "question": questao,
            "answer": ""  # sera preenchido automaticamente por preencher_respostas()
        })

    return pares_perg_resp

def preencher_respostas(pares_perg_resp):
    # Carregar um modelo de question-answering > questao_resposta
    #modelo_perg_resp = "huawei-noah/TinyBERT_General_4L_312D" NAO FUNFOU BEM se nao declarar essa variavel, ele vai por um modelo padrao
    #pr_pipeline = pipeline("question-answering", model=modelo_perg_resp, tokenizer=modelo_perg_resp)
    modelo_perg_resp = "deepset/roberta-base-squad2"  # Modelo RoBERTa ajustado para QA
    #modelo_perg_resp = "distilbert-base-cased-distilled-squad"
    pr_pipeline = pipeline("question-answering", model=modelo_perg_resp, tokenizer=modelo_perg_resp)

    for par in pares_perg_resp:
        contexto = par["context"]
        questao = par["question"]
        # Extrair a resposta automaticamente
        result = pr_pipeline(question=questao, context=contexto)
        par["answer"] = result["answer"]

    return pares_perg_resp

# Funcao para processar documentos em uma pasta
def processar_documentos(caminho_pasta_arquivos):
    questoes_dataset = []
    for filename in os.listdir(caminho_pasta_arquivos):
        file_path = os.path.join(caminho_pasta_arquivos, filename)
        if filename.endswith(".pdf"):
            texto = extrair_texto_pdf(file_path)
        elif filename.endswith(".docx"):
            texto = extrair_texto_docx(file_path)
        elif filename.endswith(".txt"):
            texto = extrair_texto_txt(file_path)
        else:
            continue  # Ignorar outros tipos de arquivo

        # Gerar perguntas e respostas
        pares_pergunta_resposta = gerar_pr_pares(texto)
        questoes_dataset.extend(pares_pergunta_resposta)

    #preencher as respostas automaticamente
    questoes_dataset = preencher_respostas(questoes_dataset)

    return questoes_dataset

# Funcao para treinar o modelo
def treinar_modelo(questoes_dataset):
    # Converter o conjunto de dados para o formato do Hugging Face
    dataset = Dataset.from_dict({
        "context": [item["context"] for item in questoes_dataset],
        "question": [item["question"] for item in questoes_dataset],
        "answer": [item["answer"] for item in questoes_dataset]
    })

    # mostra o tamanho do conjunto de dados do dataset. ele nao pode ser maior que o range do dataset abaixo.
    print(f"Tamanho do conjunto de dados: {len(dataset)}")

    #Limita o numero de exemplos ao tamanho do dataset
    tamanho_max_ds = min(len(dataset), 1000)

    # Embaralhar o conjunto de dados e selecionar os primeiros 1.000 exemplos (mais rapido). retire se tiver prejudicando GPU
    dataset = dataset.shuffle(seed=42).select(range(tamanho_max_ds))

    # Tokenizar os dados
    #dados_tokenizados = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    #modelo_treinamento = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased")

    # Tokenizar os dados (versao do bert menor, para ser mais rapido)
    #dados_tokenizados = AutoTokenizer.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
    #modelo_treinamento = AutoModelForQuestionAnswering.from_pretrained("huawei-noah/TinyBERT_General_4L_312D")
    #dados_tokenizados = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
    #modelo_treinamento = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad")
    dados_tokenizados = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    modelo_treinamento = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

    def funcao_preprocessadora(examples):
        inputs = dados_tokenizados(
            examples["question"],
            examples["context"],
            truncation=True,
            padding="max_length",
            max_length=512,
            return_tensors="pt"
        )
        # Encontrar as posições de início e fim das respostas
        inputs["start_positions"] = [
            examples["context"][i].find(examples["answer"][i]) for i in range(len(examples["answer"]))
        ]
        inputs["end_positions"] = [
            examples["context"][i].find(examples["answer"][i]) + len(examples["answer"][i])
            for i in range(len(examples["answer"]))
        ]
        return inputs

    # Aplicar o pre-processamento
    dataset_tokenizado = dataset.map(funcao_preprocessadora, batched=True)

    # Configurar o treinamento
    argumentos_treinamentos = TrainingArguments(
        output_dir="./resultados",
        per_device_train_batch_size=8, # passar 8 exemplos por vez para o processador
        num_train_epochs=3, # epocas do treinamento. o modelo passara pelos dados gerados 3 vezes
        save_steps=100, #Salva checkpoints a cada 500 passos
        #save_steps=10_000,
        save_total_limit=2,
        logging_dir="./logs",
    )

    treinador = Trainer(
        model=modelo_treinamento,
        args=argumentos_treinamentos,
        train_dataset=dataset_tokenizado,
    )

    # Treinar o modelo
    treinador.train()

    # Salvar o modelo treinado
    modelo_treinamento.save_pretrained("./meu_modelo_ajustado")
    dados_tokenizados.save_pretrained("./meu_modelo_ajustado")

    print("Modelo treinado e salvo com sucesso!")

# Pasta contendo os documentos
diretorio_documentos = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\arquivos_base"

# Processar documentos e gerar o conjunto de dados
perg_resp_dataset = processar_documentos(diretorio_documentos)

# Salvar o conjunto de dados em um arquivo JSON
with open("pr_dataset.json", "w", encoding="utf-8") as arq_json:
    json.dump(perg_resp_dataset, arq_json, ensure_ascii=False, indent=4)

# Treinar o modelo com o conjunto de dados gerado
treinar_modelo(perg_resp_dataset)