import pytest
from main_pipeline_chain_responsability import AlertaContexto, MontaPromptPasso, EnriquecerComHistoriaPasso


def test_monta_prompt_passo_sem_historico():
    """
    Testa se o prompt é montado corretamente quando NÃO HÁ histórico do Redis.
    """
    # 1. PREPARAÇÃO (Arrange)
    # Criamos um objeto de contexto com dados de teste simples.
    contexto = AlertaContexto(
        grupo="Servidores Web",
        descricao="Alta latência na porta 443",
        expressao="{host:item.avg(5m)} > 100",
        expressao_recuperada="{host:item.avg(5m)} < 50"
    )
    # O atributo 'historico' começa vazio, simulando um alerta inédito.

    # Criamos uma instância da classe que queremos testar.
    passo = MontaPromptPasso()

    # 2. AÇÃO (Act)
    # Executamos o método que queremos testar.
    contexto_processado = passo.processa(contexto)

    # 3. VERIFICAÇÃO (Assert)
    # Verificamos se o resultado é o esperado. `assert` falhará o teste se a condição for falsa.
    assert "Você é um assistente de engenharia de redes" in contexto_processado.prompt_sistema
    assert "Aja como um especialista na classe de equipamento 'Servidores Web'" in contexto_processado.prompt_usuario
    assert "Alta latência na porta 443" in contexto_processado.prompt_usuario
    # Como não havia histórico, a string "Contexto Histórico Adicional" não deve estar no prompt.
    assert "Contexto Histórico Adicional" not in contexto_processado.prompt_usuario

def test_monta_prompt_passo_com_historico():
    """
    Testa se o prompt é montado corretamente quando HÁ um histórico vindo do Redis.
    """
    # 1. PREPARAÇÃO (Arrange)
    contexto = AlertaContexto(
        grupo="Servidores Web",
        descricao="Alta latência na porta 443",
        expressao="{host:item.avg(5m)} > 100",
        expressao_recuperada="{host:item.avg(5m)} < 50"
    )
    # Simulamos que a etapa anterior (do Redis) preencheu o campo de histórico.
    contexto.historico = "--- Contexto Histórico Adicional --- Sugestão anterior: reinicie o serviço."

    passo = MontaPromptPasso()

    # 2. AÇÃO (Act)
    contexto_processado = passo.processa(contexto)

    # 3. VERIFICAÇÃO (Assert)
    # Agora, a string de histórico DEVE estar presente no prompt final.
    assert "Sugestão anterior: reinicie o serviço." in contexto_processado.prompt_usuario

# Esta classe depende do Redis. Em um teste de unidade, não queremos nos conectar
# a um Redis de verdade.

def test_enriquecer_com_historico_quando_chave_existe(mocker):
    # 1. PREPARAÇÃO (Arrange)
    # Criamos um mock que se comporta como o cliente Redis.
    mock_redis_cliente = mocker.MagicMock()

    # Quando 'exists' for chamado, deve retornar True.
    mock_redis_cliente.exists.return_value = True
    # Quando 'hgetall' for chamado, deve retornar um dicionário de teste.
    mock_redis_cliente.hgetall.return_value = {
        'ultima_sugestao': 'Verificar o balanceador de carga.',
        'count': '3'
    }

    contexto = AlertaContexto("DBs", "Slow Query", "expr1", "expr2")
    # Instanciamos nosso passo, mas passamos o MOCK no lugar do cliente real.
    passo = EnriquecerComHistoriaPasso(cliente_redis=mock_redis_cliente)

    # 2. AÇÃO (Act)
    contexto_processado = passo.processa(contexto)

    # 3. VERIFICAÇÃO (Assert)
    # Verificamos se o método 'exists' do nosso mock foi chamado uma vez.
    mock_redis_cliente.exists.assert_called_once()
    # Verificamos se o método 'hgetall' também foi chamado.
    mock_redis_cliente.hgetall.assert_called_once()

    # Verificamos se o contexto foi preenchido com os dados do mock.
    assert "Verificar o balanceador de carga" in contexto_processado.historico
    assert "Contagem de Ocorrências: 3" in contexto_processado.historico
    # Verificamos se o atributo dinâmico 'redis_chave' foi adicionado.
    assert hasattr(contexto_processado, 'redis_chave')


def test_enriquecer_com_historico_quando_chave_nao_existe(mocker):
    """
    Testa o caminho alternativo: o alerta é novo e a chave não existe no Redis.
    """
    # 1. PREPARAÇÃO (Arrange)
    mock_redis_cliente = mocker.MagicMock()
    # Desta vez, 'exists' deve retornar False.
    mock_redis_cliente.exists.return_value = False

    contexto = AlertaContexto("DBs", "Slow Query", "expr1", "expr2")
    passo = EnriquecerComHistoriaPasso(cliente_redis=mock_redis_cliente)

    # 2. AÇÃO (Act)
    contexto_processado = passo.processa(contexto)

    # 3. VERIFICAÇÃO (Assert)
    # Verificamos que 'exists' foi chamado.
    mock_redis_cliente.exists.assert_called_once()
    # MUITO IMPORTANTE: verificamos que 'hgetall' NÃO foi chamado,
    # pois não faria sentido buscar dados de uma chave que não existe.
    mock_redis_cliente.hgetall.assert_not_called()

    # O histórico deve permanecer vazio.
    assert contexto_processado.historico == ""

