# Título
# Projeto de Automação de Subida de Projetos para GitHub

## Descrição curta
Este projeto tem como objetivo automatizar a subida de projetos para o GitHub, criando um arquivo `README.md` funcional e configurando o `.gitignore` com a ajuda de Inteligência Artificial (IA).

## Principais Conceitos
* Automação de tarefas de subida de projetos para o GitHub
* Criação de arquivos `README.md` e `.gitignore` com auxílio de IA
* Utilização do GitHub CLI para autenticação e subida de projetos
* Necessidade de Python 3.11 ou superior para execução do script

## Como usar
Para utilizar este projeto, siga os passos abaixo:
1. **Instale o Python 3.11 ou superior** em sua máquina.
2. **Instale o Git e o GitHub CLI (gh)**:
	* No Windows:
		+ Instalar o Git: <https://git-scm.com/downloads>
		+ Instalar o GitHub CLI (gh): <https://cli.github.com/>
	* No Linux (Arch):
		+ `sudo pacman -S git`
		+ `sudo pacman -S github-cli`
3. **Configure o GitHub CLI (gh) com suas credenciais**:
	* Execute o comando `gh auth login`
	* Selecione a opção "HTTPS" como forma de acesso ao seu GitHub
	* Autentique-se com suas credenciais (não esqueça de ativar a autenticação de 2 fatores, se necessário)
4. **Execute o script** para criar o arquivo `README.md` e configurar o projeto para subida no GitHub

## Contato
Para mais informações ou sugestões, sinta-se à vontade para entrar em contato. Este projeto é opensource e qualquer contribuição é bem-vinda!