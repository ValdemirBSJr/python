# Automatizador de README.md e Subida para GitHub
=====================================================

## Descrição Curta
Este projeto utiliza Python e IA (Groq) para automatizar a criação de README.md e subida de projetos para o GitHub.

## Principais Conceitos
* Utilização de Python 3.11 ou superior
* Instalação do Git e GitHub CLI (gh)
* Configuração do gh com credenciais
* Utilização da IA da Groq para criar README.md
* Subida de projetos para o GitHub

## Como Usar
1. Instale o Python 3.11 ou superior
2. Instale o Git e o GitHub CLI (gh) seguindo as instruções abaixo:
 * Windows: https://git-scm.com/downloads e https://cli.github.com/
 * Linux (Arch): `sudo pacman -S git` e `sudo pacman -S github-cli`
3. Configure o gh com suas credenciais utilizando o comando `gh auth login`
4. Instale as dependências necessárias
5. Execute o script `run.sh` para iniciar a instalação das dependências
6. Preencha as informações solicitadas (texto do artigo, link do artigo, tecnologias usadas) para criar a postagem
7. Selecione a pasta do projeto que você deseja subir para o GitHub
8. O script criará o `.gitignore` e o `README.md` no diretório do projeto
9. Selecione um repositório existente para subir o projeto ou crie um novo repositório

## Contato
Se tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato. Este projeto é open-source e qualquer contribuição é bem-vinda!