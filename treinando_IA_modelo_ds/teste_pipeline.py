from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import os


# Funções para extrair texto de diferentes formatos
def extrair_texto_pdf(caminho_pdf):
    from PyPDF2 import PdfReader
    leitor = PdfReader(caminho_pdf)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()
    return texto


def extrair_texto_docx(caminho_docx):
    from docx import Document
    docx = Document(caminho_docx)
    texto = ""
    for paragrafo in docx.paragraphs:
        texto += paragrafo.text + "\n"
    return texto


def extrair_texto_txt(caminho_txt):
    with open(caminho_txt, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


# Função para carregar todos os documentos como contexto
def carregar_contexto(diretorio_documentos):
    contexto = ""
    for filename in os.listdir(diretorio_documentos):
        file_path = os.path.join(diretorio_documentos, filename)
        if filename.endswith(".pdf"):
            texto = extrair_texto_pdf(file_path)
        elif filename.endswith(".docx"):
            texto = extrair_texto_docx(file_path)
        elif filename.endswith(".txt"):
            texto = extrair_texto_txt(file_path)
        else:
            continue  # Ignorar outros tipos de arquivo
        contexto += texto + "\n\n"  # Adicionar o texto ao contexto
    return contexto


# Função para responder perguntas
def responder_pergunta(contexto, pergunta, tokenizer, model):
    # Tokenizar a entrada
    inputs = tokenizer(pergunta, contexto, return_tensors="pt", truncation=True, max_length=512)
    print("Tokens da entrada:", tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))

    with torch.no_grad():
        outputs = model(**inputs)

    # Encontrar o índice do token [SEP]
    sep_index = inputs["input_ids"][0].tolist().index(tokenizer.sep_token_id)
    print(f"Índice do token [SEP]: {sep_index}")

    # Limitar os logits aos tokens após [SEP]
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    start_logits[0][:sep_index + 1] = float('-inf')  # Ignorar tokens antes ou no [SEP]
    end_logits[0][:sep_index + 1] = float('-inf')  # Ignorar tokens antes ou no [SEP]

    # Obter os índices de início e fim da resposta
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits) + 1

    # Garantir que os índices sejam válidos
    if start_index >= len(inputs["input_ids"][0]) or end_index > len(inputs["input_ids"][0]):
        print("Índices fora dos limites.")
        return "Resposta não encontrada."

    # Forçar end_index > start_index
    if start_index >= end_index:
        print("Índices inválidos: start_index >= end_index")
        # Tentar ajustar end_index para ser maior que start_index
        end_index = start_index + 1
        if end_index > len(inputs["input_ids"][0]):
            return "Resposta não encontrada."

    print(f"Índice de início: {start_index.item()}, Índice de fim: {end_index.item()}")

    # Tokens da resposta
    resposta_tokens = inputs["input_ids"][0][start_index:end_index]
    print("Tokens da resposta:", tokenizer.convert_ids_to_tokens(resposta_tokens))

    # Decodificar a resposta usando batch_decode
    resposta = tokenizer.batch_decode(resposta_tokens.unsqueeze(0), skip_special_tokens=True)[0]
    print("Resposta decodificada:", resposta)

    # Forçar limpeza da resposta
    resposta = " ".join(resposta.split())  # Remove espaços extras
    if not resposta.strip():
        return "Resposta não encontrada."

    return resposta


# Loop principal para interação com o usuário
def main():
    print("Bem-vindo ao assistente de perguntas e respostas!")
    print("Digite 'sair' a qualquer momento para encerrar o programa.\n")

    # Diretório contendo os documentos usados para treinar o modelo
    diretorio_documentos = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\arquivos_base"

    # Carregar o contexto a partir dos documentos
    print("Carregando contexto a partir dos documentos...")
    contexto = carregar_contexto(diretorio_documentos)
    if not contexto.strip():
        print("Contexto vazio. Encerrando o programa.")
        return

    print("Contexto carregado com sucesso!\n")

    # Carregar o modelo ajustado e o tokenizador
    print("Carregando o modelo ajustado...")
    modelo = AutoModelForQuestionAnswering.from_pretrained("./meu_modelo_ajustado")
    tokenizer = AutoTokenizer.from_pretrained("./meu_modelo_ajustado")
    print("Modelo carregado com sucesso!\n")

    while True:
        # Receber a pergunta do usuário
        pergunta = input("\nDigite sua pergunta: ").strip()

        # Verificar se o usuário deseja sair
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o programa. Até logo!")
            break

        # Gerar e exibir a resposta
        resposta = responder_pergunta(contexto, pergunta, tokenizer, modelo)
        print(f"\nResposta: {resposta}")


# Executar o programa
if __name__ == "__main__":
    main()