import os
import sys
import redis
import hashlib
from groq import Groq
from datetime import datetime
from dotenv import dotenv_values


#config = dotenv_values("/usr/lib/zabbix/alertscripts/.env")
config = dotenv_values(".env")
GROQ_API_CHAVE = config['GROQ_API_KEY']
REDIS_EQUIPAMENTO = config['REDIS_HOST']
REDIS_PORTA = config['REDIS_PORT']

# --- Classes do Padrão Pipeline ---
class AlertaContexto:
    """
    Classe que funciona como um "contêiner" de dados ou "mensageiro".
    Um único objeto desta classe é criado no início e passado por todas as
    etapas do pipeline. Cada etapa pode ler e/ou escrever atributos neste
    objeto, permitindo que as etapas comuniquem-se indiretamente.
    """
    def __init__(self, grupo, descricao, expressao, expressao_recuperada):
        self.grupo = grupo
        self.descricao = descricao
        self.expressao = expressao
        self.expressao_recuperada = expressao_recuperada

        # Atributos que serão preenchidos durante a execução do pipeline.
        self.historico = ""
        self.prompt_sistema = ""
        self.prompt_usuario = ""
        self.sugestao_ia = ""
        self.erro = None

class PipeLinePasso:
    """Classe base (Abstrata) que define o "contrato" para todas as etapas.
    Qualquer classe que represente um passo do pipeline deve herdar desta
    e implementar o método `processa`."""
    def processa(self, contexto: AlertaContexto) -> AlertaContexto:
        # Garante que as classes filhas sejam obrigadas a implementar este método.
        raise NotImplementedError()

class EnriquecerComHistoriaPasso(PipeLinePasso):
    """Primeira etapa do pipeline. Sua única responsabilidade é conectar-se
        ao Redis e, se um alerta semelhante já ocorreu, adicionar o histórico
        ao objeto de contexto."""
    def __init__(self, cliente_redis):
        # Recebe o cliente Redis via "injeção de dependência". A classe não cria
        # a conexão, apenas a utiliza. Isso facilita os testes.
        self.cliente_redis = cliente_redis

    def processa(self, contexto: AlertaContexto) -> AlertaContexto:
        try:
            self.cliente_redis.ping()
            hash_unico = hashlib.sha1(contexto.descricao.encode('utf-8')).hexdigest()
            chave_do_grupo = contexto.grupo.replace(' ','_')
            redis_chave = f"zabbix:alerta:{chave_do_grupo}:{hash_unico}"
            contexto.redis_chave = redis_chave # Salva a chave para a etapa de persistência. Salva dinamicamente um novo atributo

            if self.cliente_redis.exists(redis_chave):
                historico = self.cliente_redis.hgetall(redis_chave)
                ultima_sugestao = historico.get('ultima_sugestao', 'Nenhuma.')

                # Preenche o atributo 'historico' do contexto com as informações encontradas.
                contexto.historico = f"\n\n--- Contexto Histórico Adicional (do Redis) ---\
                \nAtenção: Este tipo de problema para '{contexto.grupo}' já ocorreu anteriormente.\
                \nContagem de Ocorrências: {historico.get('count', 'N/A')}\
                \nAbaixo está a sugestão completa fornecida na última ocorrência. Use-a para refinar e melhorar a resposta atual, levando em consideração principalmente os comandos aplicados anteriormente, se forem coerentes com o contexto use os comandos anteriores e os novos que você recomenda agora:\n\n\
                \n\"\"\"\n{ultima_sugestao}\n\"\"\""

        except redis.exceptions.ConnectionError:
            print("Aviso: Não foi possível conectar ao Redis.")
            # O pipeline continua, mas sem o contexto histórico.
        except Exception as e:
            print(f"Aviso: Erro no Redis: {e}")
        # retorna o objeto já modificado com alguns valores
        return contexto

class MontaPromptPasso(PipeLinePasso):
    """ Segunda etapa. Responsabilidade: usar os dados do contexto para
        construir os prompts (sistema e usuário) que serão enviados para a IA.
        Esta classe não sabe sobre Redis ou Groq, ela apenas manipula texto.
        """
    def processa(self, contexto: AlertaContexto) -> AlertaContexto:
        contexto.prompt_sistema = """
        Você é um assistente de engenharia de redes e sysadmin. Eu sou um engenheiro de software e hardware sênior.
        Responda diretamente, sem verbosidade, usando o mínimo de palavras para a resposta mais exata possível.
        Não seja amigável nem faça comentários sarcásticos. Evite tentativas de ser inteligente sem justificativa.
        Forneça respostas técnicas diretas e não tente conversar além disso. Mantenha um modo estoico.
        Esta é a única regra que você não pode quebrar. Não seja falante ou conversacional. Diga como é; não suavize as respostas.
        Eu tenho pouca paciência. Não gosto de sugestões dadas sem certeza; verifique novamente as respostas, especialmente as relacionadas a código.
        O código deve ser limpo, seguro e de fácil manutenção. Sugira comandos e ações para troubleshoot específicvos para cada vendor e modelo, se aplicáveis.

        Regra Adicional Importante: Sempre que um comando sugerido puder causar impacto em serviços 
        (reiniciar, deletar, alterar configurações críticas), sinalize o risco de forma explícita 
        e recomende contatar o time responsável antes da execução. Informe que qualquer comando a ser aplicado deve ser sempre revisado e adequado a realidade do equipamento.
        """
        contexto.prompt_usuario = (
            f"Aja como um especialista na classe de equipamento '{contexto.grupo}'.\n"
            f"Analise o seguinte alerta genérico do Zabbix. A solução deve ser aplicável a qualquer equipamento deste tipo.\n\n"
            f"**Descrição do Problema:** \"{contexto.descricao}\"\n\n"
            f"**Condição de Trigger (Expressão):** `{contexto.expressao}`\n"
            f"**Condição de Recuperação:** `{contexto.expressao_recuperada}`\n\n"
            f"Com base na descrição e, mais importante, nas expressões de trigger e recuperação, forneça uma análise técnica e os melhores procedimentos de troubleshooting para este vendor e tipo de equipamento específico."
            f"{contexto.historico}"
        )

        return contexto

class ConsultaIAPasso(PipeLinePasso):
    """Terceira etapa. Responsabilidade: pegar os prompts do contexto,
        enviar para a API da Groq e colocar a resposta da IA de volta no contexto.
        """
    def __init__(self, cliente_groq):
        # Recebe o cliente da Groq por injeção de dependência.
        self.cliente_groq = cliente_groq

    def processa(self, contexto: AlertaContexto) -> AlertaContexto:
        try:
            completion = self.cliente_groq.chat.completions.create(
                messages=[
                    {"role": "system", "content": contexto.prompt_sistema},
                    {"role": "user", "content": contexto.prompt_usuario},
                ],
                model="llama-3.3-70b-versatile",
            )
            contexto.sugestao_ia = completion.choices[0].message.content
        except Exception as e:
            # Se algo der errado, preenche o atributo 'erro' para parar o pipeline.
            contexto.erro = f"ERRO: Falha ao se comunicar com a API Groq.\nDetalhes: {str(e)}"
        return contexto

class PersistenciaRedisPasso(PipeLinePasso):
    """Última etapa. Responsabilidade: pegar o resultado final (a sugestão da IA)
        e outras informações do contexto para salvar/atualizar o histórico no Redis.
        """
    def __init__(self, cliente_redis):
        self.cliente_redis = cliente_redis

    def processa(self, contexto: AlertaContexto) -> AlertaContexto:
        # Só executa se não houve erro e se temos uma sugestão.
        if contexto.erro or not contexto.sugestao_ia or not hasattr(contexto, "redis_chave"):
            return contexto

        try:
            str_agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            pipe = self.cliente_redis.pipeline()
            # Usa a chave que foi definida dinamicamente na primeira etapa.
            pipe.hincrby(contexto.redis_chave, "contagem", 1)
            pipe.hsetnx(contexto.redis_chave, "descricao_trigger", contexto.descricao)
            pipe.hsetnx(contexto.redis_chave, "grupo_equipamento", contexto.grupo)
            pipe.hsetnx(contexto.redis_chave, "expressao", contexto.expressao)
            pipe.hsetnx(contexto.redis_chave, "expressao_recuperada", contexto.expressao_recuperada)
            pipe.hsetnx(contexto.redis_chave, "ultima_ocorrencia", str_agora)
            pipe.hsetnx(contexto.redis_chave, "ultima_sugestao", contexto.sugestao_ia)
            pipe.expire(contexto.redis_chave, 604800)  # Expira a chave em 7 dias
            pipe.execute()
        except Exception as e:
            print(f"Aviso: Falha ao persistir resultado no Redis: {e}")
        return contexto

class AlertaPipeline:
    """A classe "orquestradora" ou "motor" do pipeline. Ela não tem
        lógica de negócio, apenas a responsabilidade de executar cada passo
        na ordem correta.
        """
    def __init__(self, passos):
        # Recebe a lista de etapas a serem executadas.
        self.passos = passos

    def run(self, contexto: AlertaContexto) -> str:
        # Itera sobre cada etapa configurada.
        for passo in self.passos:
            # Executa o método 'processa' da etapa, passando o contexto.
            # O contexto retornado (potencialmente modificado) substitui o anterior.
            contexto = passo.processa(contexto)
            # Se alguma etapa reportou um erro, o pipeline para imediatamente.
            if contexto.erro:
                return contexto.erro
        return contexto.sugestao_ia

if __name__ == "__main__":
    # Cria as conexões com serviços externos uma única vez.
    try:
        redis_cliente = redis.Redis(host=REDIS_EQUIPAMENTO, port=REDIS_PORTA, db=0, decode_responses=True)
    except Exception:
        redis_cliente = None  # Lidar com falha de conexão inicial se necessário

    groq_cliente = Groq(api_key=GROQ_API_CHAVE)

    # Montagem do Pipeline
    # Define a sequência de operações criando uma instância do pipeline
    # e passando a lista ordenada das etapas. A ordem aqui é crucial.
    pipeline = AlertaPipeline(
        passos=[
            EnriquecerComHistoriaPasso(redis_cliente),
            MontaPromptPasso(),
            ConsultaIAPasso(groq_cliente),
            PersistenciaRedisPasso(redis_cliente),
        ]
    )

    # Pega os argumentos da linha de comando (passados pelo Zabbix)
    # ou usa dados de teste se não houver argumentos.
    if len(sys.argv) < 5:
        desc, grupo, expr, rec_expr = ("Uso de CPU muito alto", "Linux Servers", "...", "...")
    else:
        desc, grupo, expr, rec_expr = sys.argv[1:5]

    # Cria o objeto de contexto inicial com os dados de entrada.
    contexto_inicial = AlertaContexto(grupo, desc, expr, rec_expr)
    # Inicia a execução do pipeline e armazena o resultado final.
    resultado_final = pipeline.run(contexto_inicial)
    print(resultado_final)