#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para sincronizar usuários de múltiplos servidores LDAP de origem
para um servidor LDAP local, que funcionará como proxy para o Semaphore UI.

Este script utiliza um padrão orientado a objetos para organizar a lógica,
carrega configurações sensíveis de um arquivo .env e utiliza o módulo
de logging para fornecer feedback detalhado sobre a operação.
"""

import ldap3
import sys
import logging
from typing import Dict, Any, List

# Importa as configurações do módulo config.py
import config

# --- Configuração do Logging ---
# Define um formato padrão para as mensagens de log, tornando a saída mais clara.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class SincronizadorLDAP:
    """
    Encapsula toda a lógica de conexão, coleta e sincronização de usuários LDAP.
    """

    def __init__(self):
        """Construtor da classe. Inicializa o dicionário de usuários."""
        # Dicionário para armazenar todos os usuários únicos coletados dos servidores de origem.
        # A chave será o 'uid' e o valor será o dicionário de atributos.
        self.todos_os_usuarios: Dict[str, Dict] = {}
        self.estatisticas = {"adicionados": 0, "atualizados": 0, "erros": 0}

    def _coletar_usuarios_origem(self) -> None:
        """
        Itera sobre os servidores de origem, conecta-se a eles e coleta
        os dados dos usuários.
        """
        logging.info("--- 1. Coletando usuários dos servidores de origem ---")
        for host in config.SERVIDORES_ORIGEM:
            try:
                logging.info(f"[*] Conectando a {host}...")
                servidor = ldap3.Server(host, get_info=ldap3.ALL, connect_timeout=5)
                # O 'with' garante que a conexão será fechada (unbind) automaticamente
                with ldap3.Connection(servidor, user=config.USUARIO_ORIGEM, password=config.SENHA_ORIGEM,
                                      auto_bind=True) as conexao:
                    conexao.search(
                        search_base=config.BASE_DN_ORIGEM,
                        search_filter=config.FILTRO_BUSCA_ORIGEM,
                        attributes=config.ATRIBUTOS_PARA_COPIAR
                    )

                    contador_local = 0
                    for entrada in conexao.entries:
                        if 'uid' in entrada:
                            # entry.entry_attributes_as_dict retorna os atributos de forma mais fácil de usar
                            self.todos_os_usuarios[entrada.uid.value] = entrada.entry_attributes_as_dict
                            contador_local += 1
                    logging.info(f"    --> Encontrados {contador_local} usuários válidos em {host}.")

            except ldap3.core.exceptions.LDAPException as e:
                logging.error(f"    --> ERRO ao conectar ou buscar em {host}: {e}")
                continue

    def _preparar_atributos_destino(self, uid: str, atributos_origem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma estrutura de atributos limpa e válida para o servidor de destino,
        baseada nos dados coletados do servidor de origem.
        """
        # Define as objectClasses básicas para um usuário no LDAP local (padrão inetOrgPerson)
        novos_atributos = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'inetOrgPerson'],
            'sn': atributos_origem.get('sn', [uid])[0],  # Se 'sn' não existir, usa o 'uid' como fallback
            'cn': atributos_origem.get('cn', [uid])[0]  # Se 'cn' não existir, usa o 'uid' como fallback
        }

        # Copia apenas os atributos desejados, garantindo que não sejam vazios
        for attr in config.ATRIBUTOS_PARA_COPIAR:
            # Evita reescrever os que já foram tratados acima
            if attr in atributos_origem and attr not in ['uid', 'cn', 'sn']:
                valor = atributos_origem[attr]
                # Garante que o valor (ou a lista de valores) não é vazio
                if isinstance(valor, list):
                    valores_filtrados = [v for v in valor if v and str(v).strip()]
                    if valores_filtrados:
                        novos_atributos[attr] = valores_filtrados
                elif valor and str(valor).strip():
                    novos_atributos[attr] = valor

        return novos_atributos

    def _sincronizar_usuario(self, conexao_destino: ldap3.Connection, uid: str,
                             atributos_origem: Dict[str, Any]) -> None:
        """
        Processa um único usuário: verifica se ele existe no destino e o
        cria ou atualiza conforme necessário.
        """
        dn_destino = f"uid={uid},{config.BASE_DN_DESTINO}"

        novos_atributos = self._preparar_atributos_destino(uid, atributos_origem)

        # Validação crucial: Garante que 'cn' e 'sn' têm valores válidos antes de prosseguir
        if not novos_atributos.get('cn') or not novos_atributos.get('sn'):
            logging.warning(f"    --> Pulando {dn_destino}: 'cn' ou 'sn' ausente ou vazio.")
            return

        # Verifica se o usuário já existe no destino
        if not conexao_destino.search(dn_destino, '(objectClass=*)', attributes=['uid']):
            # Se não existe, adiciona o novo usuário
            conexao_destino.add(dn_destino, attributes=novos_atributos)
            if conexao_destino.result['result'] == 0:
                self.estatisticas["adicionados"] += 1
            else:
                logging.error(f"    --> ERRO ao adicionar {dn_destino}: {conexao_destino.result}")
                self.estatisticas["erros"] += 1
        else:
            # Se já existe, prepara a operação de modificação
            # O formato para MODIFY é um dicionário de tuplas: { 'atributo': (operação, [valores]) }
            mudancas = {}
            for attr, valor in novos_atributos.items():
                if attr != 'objectClass':  # objectClass não deve ser modificada
                    mudancas[attr] = (ldap3.MODIFY_REPLACE, valor)

            if mudancas:
                conexao_destino.modify(dn_destino, mudancas)
                if conexao_destino.result['result'] == 0:
                    self.estatisticas["atualizados"] += 1
                else:
                    logging.error(f"    --> ERRO ao atualizar {dn_destino}: {conexao_destino.result}")
                    self.estatisticas["erros"] += 1

    def executar_sincronizacao(self) -> None:
        """
        Orquestra todo o processo de sincronização.
        """
        self._coletar_usuarios_origem()

        total_usuarios = len(self.todos_os_usuarios)
        logging.info(f"\nTotal de usuários únicos a sincronizar: {total_usuarios}")
        if not total_usuarios:
            logging.info("Nenhum usuário encontrado. Encerrando.")
            return

        logging.info("\n--- 2. Sincronizando com o servidor local ---")
        try:
            servidor_destino = ldap3.Server(config.URI_SERVIDOR_DESTINO, get_info=ldap3.ALL)
            with ldap3.Connection(servidor_destino, user=config.USUARIO_ADMIN_DESTINO,
                                  password=config.SENHA_ADMIN_DESTINO, auto_bind=True) as conexao_destino:
                for uid, atributos in self.todos_os_usuarios.items():
                    self._sincronizar_usuario(conexao_destino, uid, atributos)

            logging.info("\n--- Resumo da Sincronização ---")
            logging.info(f"Novos usuários adicionados: {self.estatisticas['adicionados']}")
            logging.info(f"Usuários existentes atualizados: {self.estatisticas['atualizados']}")
            logging.info(f"Erros encontrados: {self.estatisticas['erros']}")

        except ldap3.core.exceptions.LDAPException as e:
            logging.critical(f"ERRO FATAL durante a sincronização com o servidor local: {e}")
            sys.exit(1)


def main():
    """Função principal que inicia o processo."""
    try:
        sincronizador = SincronizadorLDAP()
        sincronizador.executar_sincronizacao()
    except ValueError as e:
        # Captura erros de configuração do config.py
        logging.critical(f"Erro de configuração: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Ocorreu um erro inesperado no script: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
