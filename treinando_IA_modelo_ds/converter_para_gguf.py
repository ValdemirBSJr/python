import onnx
import numpy as np
from gguf import GGUFWriter


# Caminho do modelo ONNX de entrada
caminho_modelo_onnx = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\model.onnx"
caminho_pesos = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\pesos.npz"
caminho_gguf = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\model.gguf"
caminho_modelfile = r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\meu-modelo-teste.modelfile"

# Carregar o modelo ONNX

print("Carregando modelo ONNX...")
onnx_modelo = onnx.load(caminho_modelo_onnx)

# Extrair informações do modelo ONNX (pesos e configurações)
print("Extraindo pesos e configurações do modelo...")
pesos = {}
for initializer in onnx_modelo.graph.initializer:
    pesos[initializer.name] = np.frombuffer(initializer.raw_data, dtype=np.float32).reshape(initializer.dims)

# Salvar os pesos em um formato compatível com GGUF
print("Convertendo os pesos para NPZ...")
# Aqui, usamos a API do llama-cpp-python para salvar no formato GGUF
np.savez(r"C:\Users\N5669203\Documents\PycharmProjects\treinando_IA_modelo_ds\modelo_onnx\pesos.npz", **pesos)

print("Carregando pesos...")

pesos = np.load(caminho_pesos)

print("Criando arquivo GGUF...")

escrever_gguf = GGUFWriter(caminho_gguf, "Modelo Ajustado")

#Adicionando os pesos ao GGUF
for nome, valor in pesos.items():
    #print(f"Adicionando peso: {nome}")
    escrever_gguf.add_tensor(nome, valor)

escrever_gguf.write_header_to_file()
escrever_gguf.write_kv_data_to_file()
escrever_gguf.write_tensors_to_file()
escrever_gguf.close()

print("Modelo convertido com sucesso!")

#Criar o ModelFile
print("Criando ModelFile...")

with open(caminho_modelfile, "w") as f:
    f.write(f"FROM {caminho_gguf}\n")
    f.write("TEMPLATE \"\"\"\n")
    f.write("{{ if .System }}{{ .System }}\n{{ end }}")
    f.write("{{ if .Prompt }}{{ .Prompt }}{{ end }}")
    f.write("{{ if .Response }}{{ .Response }}{{ end }}")
    f.write("\"\"\"\n")
    f.write("PARAMETER stop [\"\"]\n")
    f.write("PARAMETER num_ctx 2048\n")
    f.write("LICENSE MIT\n")

print("ModelFile criado com sucesso!")





