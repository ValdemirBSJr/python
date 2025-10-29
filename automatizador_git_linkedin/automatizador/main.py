import os
import sys
import json
import stat
import shutil
import tempfile
import subprocess
import tkinter as tk
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, List, Dict, Tuple
from tkinter import simpledialog, messagebox, filedialog, scrolledtext, Listbox, END, Toplevel

# --- 0.1 Função para ajudar a desbloquear arquivos .git encadeados readonly ---
def rm_erro(func, path, exc_info):
    """
    Handler de erro para shutil.rmtree, caso recebamos um
    arquivo bloqueado para edção/remoção tentamos remover o atributo pra o win
    """
    try:
        # Tenta remover o atributo 'read-only'
        os.chmod(path, stat.S_IWRITE)
        # Tenta executar a função de remoção (ex: os.remove) novamente
        func(path)
    except Exception as e:
        print(f"Falha ao forçar a remoção de {path}: {e}")
        


# --- 1. Verificações de Pré-requisitos ---
def verificar_dependencias():
    """Verifica se 'git' e 'gh' estão instalados no sistema."""
    if not shutil.which('git'):
        messagebox.showerror("Erro de dependência", "O git não está instalado.")
        sys.exit(1)

    if not shutil.which('gh'):
        messagebox.showerror("Erro de dependência", "O gh (Github CLI) não está instalado.")
        sys.exit(1)

    # Verifica se o gh está autenticado
    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro de Autenticação",
                             "Você não está autenticado no 'gh'. Por favor, rode 'gh auth login' no seu terminal.")
        sys.exit(1)


# --- 2. Camada de Serviço: Groq ---
class GroqService:
    """
    Classe de serviço responsável por toda a comunicação
    com a API do Groq.
    """

    def __init__(self, api_key: str):
        if not api_key:
            messagebox.showerror("Erro de API", "A chave de API do GROQ não foi encontrada!")
            sys.exit(1)

        self.cliente = Groq(api_key=api_key)
        self.modelo = "llama-3.3-70b-versatile"

    def _fazer_requisicao(self, prompt: str) -> Optional[str]:
        """Método privado para executar a chamada à API."""
        try:
            chat_completion = self.cliente.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.modelo,
            )

            return chat_completion.choices[0].message.content
        except Exception as e:
            messagebox.showerror("Erro na api do groq", f"Não foi possível contatar a API do Groq. Erro retornado: {e}")
            return None

    def gerar_sugestao_post(self, texto_artigo: str, link_artigo: str) -> Optional[str]:
        """Gera uma sugestão de post para o LinkedIn."""
        prompt = f"""
        Com base no seguinte artigo, gere um texto curto e chamativo (use emojis)
        para uma postagem no LinkedIn, incentivando a leitura.
        Foque em capturar a atenção. Seja um pouco descontraído.

        Ao final da postagem, inclua uma chamada para ação convidativa 
        e adicione este link para o artigo: {link_artigo}

        Artigo:
        \"\"\"
        {texto_artigo}
        \"\"\"
        
        Após isso, inclua tags como #tecnologia #IA e etc, mas sendo dos conteúdos do artigo
        """
        return self._fazer_requisicao(prompt)

    def gerar_readme(self, texto_artigo: str) -> Optional[str]:
        """Gera um README.md em formato Markdown para o projeto."""
        prompt = f"""
                Com base no seguinte artigo, gere um arquivo README.md em formato Markdown
                para um projeto no GitHub. O README deve ser bem estruturado com:
                - Título
                - Descrição curta
                - Principais Conceitos (baseados no artigo)
                - Como usar (se aplicável)
                - Contato

                Artigo:
                \"\"\"
                {texto_artigo}
                \"\"\"
                """
        return self._fazer_requisicao(prompt)

    def gerar_gitignore(self, tecnologias: str) -> Optional[str]:
        """Gera um .gitignore baseado nas tecnologias informadas."""
        if not tecnologias:
            tecnologias = "python"  # Padrão

        prompt = f"""
        Gere um arquivo .gitignore otimizado para um projeto com as seguintes
        tecnologias: {tecnologias}.

        Inclua seções comuns (ex: .env, __pycache__/, venv/, .venv/, *.txt, .idea/, .egg-info/).
        Retorne APENAS o conteúdo do arquivo, sem nenhuma explicação adicional, nem comentários.
        """
        return self._fazer_requisicao(prompt)


# --- 3. Camada de Serviço: GitHub ---
class GitHubService:
    """
    Classe de serviço responsável por toda a interação
    com o sistema de arquivos e os comandos 'git' e 'gh'.
    """

    def __init__(self, pasta_projeto: Path):
        # Esta é a pasta do PROJETO, não a pasta do script.
        self.pasta_projeto = pasta_projeto

    def _executar_comando(self, comando: List[str], cwd: Path) -> Tuple[bool, str]:
        """
        Método privado para executar comandos de subprocesso de forma segura.
        Crucial: O 'cwd=cwd' garante que o comando rode na pasta do projeto.
        """
        try:
            # cwd define o diretório de trabalho do comando
            resultado = subprocess.run(comando, check=True, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
            return True, resultado.stdout
        except subprocess.CalledProcessError as e:
            return False, f"Erro ao executar comando: {' '.join(comando)}\n{e.stderr}"
        except FileNotFoundError:
            return False, f"Comando não encontrado: {comando[0]}"

    def escrever_arquivo(self, nome_arquivo: str, conteudo: str) -> bool:
        """Escreve/Sobrescreve um arquivo (README ou .gitignore) na pasta do projeto."""
        try:
            # Garante que o arquivo seja escrito na pasta correta
            caminho_arquivo = self.pasta_projeto / nome_arquivo
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
            return True
        except IOError as e:
            messagebox.showerror("Erro de Arquivo",
                                 f"Não foi possível escrever em {nome_arquivo}.\n Erro retornado: {e}")
            return False

    def listar_repositorios_remotos(self) -> Optional[List[Dict[str, str]]]:
        """Busca a lista de repositórios do usuário no GitHub usando 'gh'."""

        comando = ["gh", "repo", "list", "--limit", "100", "--json", "name,url"]

        # Executa o comando na pasta do projeto (embora 'gh' possa rodar de qualquer lugar)
        sucesso, saida = self._executar_comando(comando, cwd=self.pasta_projeto)

        if sucesso:
            try:
                return json.loads(saida)
            except json.JSONDecodeError:
                messagebox.showerror("Erro de JSON", "Não foi possível processar a lista de repos do 'gh'.")
                return None

        else:
            messagebox.showerror("Erro 'gh'", f"Não foi possível listar repositórios:\n{saida}")
            return None

    def _inicializar_git(self) -> bool:
        """Garante que o 'git init' foi executado NA PASTA DO PROJETO."""
        sucesso, _ = self._executar_comando(["git", "init"], cwd=self.pasta_projeto)
        return sucesso

    def _configurar_remoto(self, url_repo: str) -> bool:
        """
        Configura o 'origin' de forma idempotente.
        Tenta adicionar; se falhar (porque já existe), atualiza a URL.
        """
        comando_add = ["git", "remote", "add", "origin", url_repo]
        try:
            subprocess.run(comando_add, cwd=self.pasta_projeto, check=True, capture_output=True)
            return True  # Adicionado com sucesso
        except subprocess.CalledProcessError:
            # Falhou, provavelmente 'origin' já existe. Vamos atualizar.
            comando_set_url = ["git", "remote", "set-url", "origin", url_repo]
            sucesso, saida = self._executar_comando(comando_set_url, cwd=self.pasta_projeto)
            if not sucesso:
                messagebox.showerror("Erro Git", f"Falha ao configurar o remoto:\n{saida}")
            return sucesso

    def _fazer_commit_e_push(self) -> bool:
        """Adiciona todos os arquivos, faz commit e push. TUDO NA PASTA DO PROJETO."""

        # O 'self.pasta_projeto' garante que o 'git add .' só adicione
        # arquivos de dentro da pasta selecionada.
        sucesso, saida = self._executar_comando(["git", "add", "."], cwd=self.pasta_projeto)
        if not sucesso:
            messagebox.showerror("Erro Git", f"Falha no 'git add':\n{saida}")
            return False

        # Verifica se há algo para commitar
        status_sucesso, status_saida = self._executar_comando(["git", "status", "--porcelain"], cwd=self.pasta_projeto)
        if not status_saida:
            messagebox.showinfo("Git", "Nenhuma mudança para commitar.")
            return True  # Não é um erro, apenas nada a fazer

        mensagem_commit = "Adiciona/atualiza arquivos do projeto via script"
        comando_commit = ["git", "commit", "-m", mensagem_commit]
        sucesso, saida = self._executar_comando(comando_commit, cwd=self.pasta_projeto)
        if not sucesso:
            messagebox.showerror("Erro Git", f"Falha no 'git commit':\n{saida}")
            return False

        # Usamos 'HEAD' para enviar o branch atual, seja 'main' ou 'master'
        comando_push = ["git", "push", "-u", "origin", "HEAD"]
        sucesso, saida = self._executar_comando(comando_push, cwd=self.pasta_projeto)
        if not sucesso:
            messagebox.showerror("Erro Git", f"Falha no 'git push':\n{saida}")
            return False

        return True

    def criar_novo_repositorio(self, nome_repo: str) -> bool:
        """Cria um novo repo no GitHub e faz o push inicial."""
        if not self._inicializar_git():
            return False

        # O 'source="."' usa o diretório atual (cwd) como fonte,
        # que está configurado como self.pasta_projeto
        comando = [
            "gh", "repo", "create", nome_repo,
            "--public",
            "--source", ".",  # Usa o diretório (cwd) como fonte
            "--remote", "origin",
            "--push"
        ]

        # Adiciona e commita localmente PRIMEIRO
        sucesso, saida = self._executar_comando(["git", "add", "."], cwd=self.pasta_projeto)
        if not sucesso:
            messagebox.showerror("Erro Git", f"Falha no 'git add':\n{saida}")
            return False

        status_sucesso, status_saida = self._executar_comando(["git", "status", "--porcelain"], cwd=self.pasta_projeto)
        if status_saida:  # Se houver mudanças
            comando_commit = ["git", "commit", "-m", "Commit inicial"]
            sucesso, saida = self._executar_comando(comando_commit, cwd=self.pasta_projeto)
            if not sucesso:
                messagebox.showerror("Erro Git", f"Falha no 'git commit':\n{saida}")
                return False

        # Agora, cria o repo remoto e dá push
        sucesso, saida = self._executar_comando(comando, cwd=self.pasta_projeto)
        if not sucesso:
            messagebox.showerror("Erro 'gh'", f"Falha ao criar o repositório:\n{saida}")
            return False

        return True

    def publicar_em_repositorio_existente(self, url_repo: str) -> bool:
        """
        Clona o repo existente, copia a pasta do projeto para dentro dele
        como um subdiretório e faz o push.
        """

        # Pega o nome da pasta do projeto (ex: "meu-novo-projeto")
        nome_pasta_projeto = self.pasta_projeto.name

        # 1. Cria um diretório temporário para clonar o repositório
        try:
            with tempfile.TemporaryDirectory() as temp_dir_str:
                temp_dir = Path(temp_dir_str)

                # 2. Clona o repositório existente para o diretório temporário
                # (O '.' clona no diretório atual, que é temp_dir)
                comando_clone = ["git", "clone", url_repo, "."]
                sucesso, saida = self._executar_comando(comando_clone, cwd=temp_dir)
                if not sucesso:
                    messagebox.showerror("Erro Git",
                                         f"Falha ao clonar o repositório '{url_repo}'.\nVerifique a URL e suas permissões.\n{saida}")
                    return False

                # 3. Define o caminho de destino (dentro do repo clonado)
                # Ex: /pasta_temporaria/meu-novo-projeto
                caminho_destino = temp_dir / nome_pasta_projeto

                # 4. Copia a pasta inteira do projeto (self.pasta_projeto)
                # para dentro do repositório clonado, IGNORANDO a pasta .git
                try:
                    # Se a pasta de destino já existe, vamos primeiro remover o conteúdo
                    # para garantir que não haja arquivos antigos conflitantes ou submódulos quebrados.
                    if caminho_destino.exists():
                        shutil.rmtree(caminho_destino)

                    shutil.copytree(
                        self.pasta_projeto,
                        caminho_destino,
                        ignore=shutil.ignore_patterns('.git', '__pycache__', 'venv', '.venv', '.idea', '.txt', '.egg-info')
                    )
                except Exception as e:
                    messagebox.showerror("Erro de Cópia", f"Falha ao copiar arquivos para '{caminho_destino}'.\n{e}")
                    return False

                # 5. Faz o Add, Commit e Push a partir do repo clonado (temp_dir)

                # Add (adiciona a nova pasta e seus conteúdos)
                sucesso, saida = self._executar_comando(["git", "add", "."], cwd=temp_dir)
                if not sucesso:
                    messagebox.showerror("Erro Git", f"Falha no 'git add' no repo temporário.\n{saida}")
                    return False

                # Commit
                # Verifica se há algo para commitar
                status_sucesso, status_saida = self._executar_comando(["git", "status", "--porcelain"], cwd=temp_dir)
                if not status_saida:
                    messagebox.showinfo("Git",
                                        "Nenhuma mudança para commitar (os arquivos já existem e estão atualizados).")
                    return True  # Não é um erro

                mensagem_commit = f"Adiciona/atualiza projeto: {nome_pasta_projeto}"
                comando_commit = ["git", "commit", "-m", mensagem_commit]
                sucesso, saida = self._executar_comando(comando_commit, cwd=temp_dir)
                if not sucesso:
                    messagebox.showerror("Erro Git", f"Falha no 'git commit' no repo temporário.\n{saida}")
                    return False

                # Push (envia o novo commit para o branch atual)
                comando_push = ["git", "push", "origin", "HEAD"]
                sucesso, saida = self._executar_comando(comando_push, cwd=temp_dir)
                if not sucesso:
                    messagebox.showerror("Erro Git", f"Falha no 'git push' final.\n{saida}")
                    return False

                return True  # Sucesso!

        except Exception as e:
            messagebox.showerror("Erro no Processo", f"Ocorreu um erro inesperado ao processar o repositório: {e}")
            return False


# --- 4. Camada de Aplicação/UI (O Orquestrador) ---
class AutomatizadorApp:
    """
    Classe principal que orquestra a UI (Tkinter) e os serviços.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.withdraw()  # Esconde a janela principal inicial

        load_dotenv()
        self.servico_groq = GroqService(api_key=os.getenv("GROQ_API_KEY"))

        # Variáveis de estado
        self.texto_artigo: Optional[str] = None
        self.tecnologias: Optional[str] = None
        self.link_artigo: Optional[str] = None

        # Essas variáveis são preenchidas no Passo 3
        self.pasta_projeto: Optional[Path] = None
        self.servico_github: Optional[GitHubService] = None

    def iniciar(self):
        """Passo 1: Inicia o fluxo da aplicação."""
        self._obter_entrada_artigo()

    def _obter_entrada_artigo(self):
        """Passo 1 (Continuação): Abre a janela para colar o texto do artigo."""
        janela = Toplevel(self.root)
        janela.title("Passo 1: Cole seu Artigo")
        janela.geometry("600x550")

        tk.Label(janela, text="Cole o texto completo do seu artigo:",
                 font=("Arial", 12)).pack(pady=10)

        campo_texto_artigo = scrolledtext.ScrolledText(janela, wrap=tk.WORD, height=15, width=70)
        campo_texto_artigo.pack(pady=5, padx=10, fill="both", expand=True)

        tk.Label(janela, text="Link do artigo no LinkedIn:",
                 font=("Arial", 10)).pack(pady=(10, 0))

        campo_link = tk.Entry(janela, width=70)
        campo_link.pack(pady=5, padx=10, fill="x")

        tk.Label(janela, text="Tecnologias do projeto (ex: python, node, react):",
                 font=("Arial", 10)).pack(pady=(10, 0))

        campo_tecnologias = tk.Entry(janela, width=70)
        campo_tecnologias.pack(pady=5, padx=10, fill="x")

        def ao_prosseguir():
            self.texto_artigo = campo_texto_artigo.get("1.0", tk.END).strip()
            self.tecnologias = campo_tecnologias.get().strip()
            self.link_artigo = campo_link.get().strip()

            if not self.texto_artigo:
                messagebox.showwarning("Entrada Inválida", "Por favor, cole o texto do artigo.")
                return

            if not self.link_artigo:
                messagebox.showwarning("Entrada Inválida", "Por favor, insira o link do artigo.")
                return

            janela.destroy()
            self._processar_post_linkedin()  # Chama o próximo passo

        tk.Button(janela, text="Analisar Texto e Prosseguir", command=ao_prosseguir,
                  font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

        self.root.wait_window(janela)

    def _processar_post_linkedin(self):
        """Passo 2: Gera e exibe a sugestão de post do LinkedIn."""
        sugestao = self.servico_groq.gerar_sugestao_post(self.texto_artigo, self.link_artigo)

        if sugestao is None:
            self._finalizar_com_erro("Falha ao gerar sugestão do Groq.")
            return

        janela = Toplevel(self.root)
        janela.title("Passo 2: Sugestão de Postagem")
        janela.geometry("500x350")

        tk.Label(janela, text="Sugestão de postagem para o LinkedIn:",
                 font=("Arial", 12)).pack(pady=10)

        campo_sugestao = scrolledtext.ScrolledText(janela, wrap=tk.WORD, height=10, width=60)
        campo_sugestao.pack(pady=5, padx=10, fill="both", expand=True)
        campo_sugestao.insert(tk.END, sugestao)

        def gerar_nova_sugestao():
            nova_sugestao = self.servico_groq.gerar_sugestao_post(self.texto_artigo, self.link_artigo)
            if nova_sugestao:
                campo_sugestao.delete("1.0", tk.END)
                campo_sugestao.insert(tk.END, nova_sugestao)

        def ao_prosseguir():
            texto_final = campo_sugestao.get("1.0", tk.END).strip()
            self.root.clipboard_clear()
            self.root.clipboard_append(texto_final)
            messagebox.showinfo("Copiado!",
                                "O texto da postagem foi copiado para sua área de transferência.")
            janela.destroy()
            self._selecionar_pasta_projeto()  # Chama o próximo passo

        frame_botoes = tk.Frame(janela)
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text="Gerar Nova", command=gerar_nova_sugestao).pack(side=tk.LEFT, padx=10)
        tk.Button(frame_botoes, text="Copiar e Prosseguir", command=ao_prosseguir,
                  bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

        self.root.wait_window(janela)

    def _selecionar_pasta_projeto(self):
        """Passo 3: Pede ao usuário para selecionar a pasta do PROJETO."""

        messagebox.showinfo("Próximo Passo",
                            "Agora, selecione a pasta do seu projeto (a pasta que você quer enviar ao GitHub).")

        caminho_pasta = filedialog.askdirectory(title="Passo 3: Selecione a Pasta do Projeto")

        print("\n[INFO] Fazendo a varredura no diretório. Aguarde ...\n")

        if not caminho_pasta:
            self._finalizar_com_erro("Nenhuma pasta de projeto selecionada. Processo cancelado.")
            return

        # Armazena o caminho da pasta do PROJETO
        self.pasta_projeto = Path(caminho_pasta)

        # CRUCIAL: Inicializa o serviço do GitHub com a pasta selecionada.
        # Agora, todos os comandos do GitHubService (git init, add, push, write)
        # serão executados DENTRO desta pasta.
        self.servico_github = GitHubService(self.pasta_projeto)

        # O fluxo continua para o próximo passo
        self._processar_arquivos_github()


        def _processar_arquivos_github(self):
        """Passo 4: Gera e escreve os arquivos README.md e .gitignore NA PASTA DO PROJETO.
        Limpa os aninhados (.git, etc)
        """

        # 'self.servico_github' agora existe e sabe onde fica a pasta do projeto
        if self.servico_github is None:
            self._finalizar_com_erro("Erro interno: Serviço GitHub não foi inicializado.")
            return

        print(f"\n[INFO] Verificando pastas .git aninhadas em: {self.pasta_projeto}n")

        # vamos verificar os subdirtórios em busca de .git redundantes
        # a partir da pasta raiz (self.pasta_projeto).
        # topdown=True permite "podar" diretórios da busca, o que é mais eficiente.
        pastas_git_aninhadas = list(self.pasta_projeto.rglob('.git'))
        pastas_removidas = []

        if pastas_git_aninhadas:
            for pasta_git in pastas_git_aninhadas:
                # Garante que é um diretório e que realmente existe
                if pasta_git.exists() and pasta_git.is_dir():
                    try:
                        shutil.rmtree(pasta_git, onerror=rm_erro)
                        print(f"Removido repositório .git aninhado: {pasta_git}")
                        pastas_removidas.append(str(pasta_git))
                    except Exception as e:
                        messagebox.showwarning("Aviso de Limpeza",
                                               f"Não foi possível remover o .git aninhado: {pasta_git}\n{e}")

            if pastas_removidas:
                messagebox.showinfo("Limpeza de Submódulos",
                                    f"Foram encontrados e removidos {len(pastas_removidas)} repositórios .git aninhados."
                                    " Isso garante um upload limpo dos arquivos.")

        # Gerar README
        readme_conteudo = self.servico_groq.gerar_readme(self.texto_artigo)
        if not readme_conteudo or not self.servico_github.escrever_arquivo("README.md", readme_conteudo):
            messagebox.showwarning("Aviso", "Não foi possível gerar ou escrever o README.md.")

        # Gerar .gitignore
        gitignore_conteudo = self.servico_groq.gerar_gitignore(self.tecnologias)
        if not gitignore_conteudo or not self.servico_github.escrever_arquivo(".gitignore", gitignore_conteudo):
            messagebox.showwarning("Aviso", "Não foi possível gerar ou escrever o .gitignore.")

        messagebox.showinfo("Arquivos Criados",
                            f"README.md e .gitignore foram criados/atualizados em:\n{self.pasta_projeto}")

        self._decidir_repositorio()  # Próximo passo

    def _decidir_repositorio(self):
        """Passo 5: Pergunta se o usuário quer um repo novo ou existente."""
        resposta = messagebox.askyesno("Passo 5: Repositório GitHub",
                                       "Deseja criar um NOVO repositório para este projeto?\n\n"
                                       "(Clique 'Não' para publicar em um repositório existente)")

        if resposta:  # Sim, criar novo
            self._criar_novo_repositorio()
        else:  # Não, usar existente
            self._selecionar_repo_existente()

    def _criar_novo_repositorio(self):
        """Passo 6 (Opção A): Pede o nome e cria o novo repositório."""
        nome_repo = simpledialog.askstring("Novo Repositório",
                                           "Digite o nome para o novo repositório (ex: meu-projeto-incrivel):")

        if not nome_repo:
            self._finalizar_com_erro("Nome do repositório inválido.")
            return

        if self.servico_github.criar_novo_repositorio(nome_repo):
            messagebox.showinfo("Sucesso!", f"Projeto publicado com sucesso no novo repositório: {nome_repo}")
            self._finalizar_script()
        else:
            self._finalizar_com_erro("Falha ao criar repositório. Verifique os logs de erro.")

    def _selecionar_repo_existente(self):
        """Passo 6 (Opção B): Lista os repositórios para seleção."""
        repos = self.servico_github.listar_repositorios_remotos()
        if repos is None:
            self._finalizar_com_erro("Não foi possível listar os repositórios.")
            return

        janela = Toplevel(self.root)
        janela.title("Selecione um Repositório Existente")
        janela.geometry("400x400")

        tk.Label(janela, text="Selecione o repositório para o push:").pack(pady=10)
        listbox = Listbox(janela, height=15, width=60)
        listbox.pack(pady=5, padx=10, fill="both", expand=True)

        mapa_repos = {}
        for repo in repos:
            nome = repo['name']

            url = repo.get('url')  # Usar .get() para segurança

            if url:  # Só adiciona se a URL existir
                mapa_repos[nome] = url
                listbox.insert(END, nome)

        def ao_selecionar():
            try:
                selecionado_index = listbox.curselection()[0]
                nome_selecionado = listbox.get(selecionado_index)
                url_selecionada = mapa_repos[nome_selecionado]

                janela.destroy()

                if self.servico_github.publicar_em_repositorio_existente(url_selecionada):
                    messagebox.showinfo("Sucesso!",
                                        f"Projeto publicado com sucesso no repositório: {nome_selecionado}")
                    self._finalizar_script()
                else:
                    self._finalizar_com_erro("Falha ao publicar em repositório existente.")

            except IndexError:
                messagebox.showwarning("Seleção Inválida", "Por favor, selecione um repositório da lista.")

        tk.Button(janela, text="Publicar neste Repositório", command=ao_selecionar,
                  bg="#4CAF50", fg="white").pack(pady=10)

        self.root.wait_window(janela)

    def _finalizar_script(self):
        """Fecha a aplicação de forma limpa."""
        self.root.destroy()
        sys.exit(0)

    def _finalizar_com_erro(self, mensagem: Optional[str] = None):
        """Fecha a aplicação em caso de erro ou cancelamento."""
        if mensagem:
            messagebox.showerror("Processo Cancelado ou com Erro", mensagem)
        self.root.destroy()
        sys.exit(1)


# --- 5. Ponto de Entrada da Aplicação ---
def iniciar_aplicacao():
    """Função de entrada principal chamada pelo 'meu-app'."""
    # 1. Verifica se 'git' e 'gh' estão prontos
    verificar_dependencias()

    # 2. Configura a raiz do Tkinter
    root = tk.Tk()

    # 3. Cria e inicia a aplicação
    app = AutomatizadorApp(root)
    app.iniciar()  # O fluxo agora é controlado 100% dentro da classe

    # 4. Mantém a aplicação rodando (necessário se alguma janela não modal for usada)
    # Como usei 'wait_window' em tudo, o script pausará em cada janela. Necessário para os inputs
    # Se 'iniciar' retornar sem fechar, o mainloop() garante que a 'root' (mesmo oculta)
    # mantenha o script vivo para os processos de clipboard, etc.
    root.mainloop()


if __name__ == "__main__":
    iniciar_aplicacao()
