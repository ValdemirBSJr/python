# Automatizador de README e Upload para GitHub
==============================================

## Descrição Curta
Este projeto utiliza Python e IA (Groq) para automatizar a criação de README.md e o upload de projetos para o GitHub.

## Principais Conceitos
* Automação de criação de README.md utilizando IA (Groq)
* Upload de projetos para o GitHub utilizando GitHub CLI (gh)
* Utilização de Python 3.11 ou superior
* Configuração do GitHub CLI (gh) com credenciais e autenticação de 2 fatores

## Como Usar
1. Instalar Python 3.11 ou superior
2. Instalar o Git e o GitHub CLI (gh) em sua máquina
 * Windows: [Git](https://git-scm.com/downloads) e [GitHub CLI](https://cli.github.com/)
 * Linux (Arch): `sudo pacman -S git` e `sudo pacman -S github-cli`
3. Configurar o GitHub CLI (gh) com credenciais utilizando o comando `gh auth login`
4. Clonar o repositório e executar o script `main.py`
5. Preencher as informações do projeto (texto, link do artigo, tecnologias usadas)
6. Selecionar a pasta do projeto e o repositório para upload
7. O script criará o README.md e o .gitignore utilizando a IA (Groq) e fará o upload do projeto para o GitHub

## Contato
Se tiver alguma dúvida ou precisar de ajuda, por favor entre em contato comigo pelo [LinkedIn](https://www.linkedin.com/in/seu-nome-de-usuario/).

## Requisitos
* Python 3.11 ou superior
* Git
* GitHub CLI (gh)
* Configuração do GitHub CLI (gh) com credenciais e autenticação de 2 fatores

## Notas
* Certifique-se de que o seu Git esteja configurado com email e nome do utilizador ou edite o `main.py` para omitir essa parte
* Se não seguir essas instruções, você pode receber um erro do Git durante o upload