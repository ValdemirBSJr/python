# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import subprocess
from dominate.tags import *
from dominate.util import raw
from datetime import datetime
from os import path
import zipfile

#abaixo, dicionario que tem as cidades e os cmts E6k
cmts_NE = {
	# sigla da cidade : {HOSTNAME: IP},
       'cd1': {'XXXDTCCMT01': '127.0.0.1', 'XXXDTCCMT02': '127.0.0.2'},
       'cd2': {'XXXDTCCMT03': '127.0.0.3', 'XXXDTCCMT04': '127.0.0.4'},



}

data_atual = datetime.now()
data_formatada = data_atual.strftime('%d/%m/%Y %H:%M')


def pega_consumo(ip_cmts:str, sigla_cidade: str) -> list:

    '''
    Função que faz a consulta CMTS a CMTS de todas suas interfaces válidas.
    Pegamos o consumo e categorizamos nos 3 critérios abaixo

    :param ip_cmts: recebe o ip do cmts corrente
    :param sigla_cidade: sigla da cidade que esta sendo consultada
    :return: retornamos 3 listas com os links de consumo. Os critérios são >70<80, >80<89 e >90.
    '''

    try:

        print(f'Tentando consulta no CMTS {ip_cmts}...')

        get_Consumo_up = subprocess.getoutput(f'snmpwalk -v2c -c public {ip_cmts} SNMPv2-SMI::transmission.127.1.3.9.1.3')
        #tentar tbm a community n0cn3t
        print(f'Consulta trouxe {len(get_Consumo_up)} linhas')

    except Exception as Ex:
        print(f'Não foi possível realiza a consulta ao {ip_cmts}. Erro: {Ex}')
        pass

    #transformo o retorno em uma lista
    get_Consumo_up = get_Consumo_up.split('\n')

    ate_80 = []
    ate_90 = []
    acima_90 = []

    for up in get_Consumo_up:

        percorre_walk_up = up.split('= INTEGER:')
        consumo_up = percorre_walk_up[1].strip()
        consumo_up = int(consumo_up)
        interface_up = percorre_walk_up[0].split('.')
        interface_up_individual = interface_up[7].strip()
        up_coleta_valida = interface_up[8].strip() # 129 para True

        if up_coleta_valida == '129' and (consumo_up >= 70 and consumo_up <= 79):
            ate_80.append(f'http://path.{sigla_cidade}.site.com/nagios/noc/graficos/php/util_{ip_cmts}_{interface_up_individual}.php')
        elif up_coleta_valida == '129' and (consumo_up >= 80 and consumo_up <= 89):
            ate_90.append(f'http://path.{sigla_cidade}.site.com/nagios/noc/graficos/php/util_{ip_cmts}_{interface_up_individual}.php')
        elif up_coleta_valida == '129' and (consumo_up >= 90):
            acima_90.append(f'http://path.{sigla_cidade}.site.com/nagios/noc/graficos/php/util_{ip_cmts}_{interface_up_individual}.php')

    return ate_80, ate_90, acima_90





if __name__ == '__main__':

    #abaixo percorro todo o dicionario tratando cmts a cmts, cidade a cidade e crio a partir dele um html


    #crio a instancia do html
    meu_html = html()

    #adiciono a ele, titulo e as libs ccs e js
    meu_head = meu_html.add(head(

        meta(charset='utf-8'),

        title(f'Relatório ups travadas E6000 - {data_formatada}'),
        link(
            rel='stylesheet',
            href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
            integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u',
            crossorigin='anonymous',
        ),

        script(
            src='https://code.jquery.com/jquery-3.5.1.slim.min.js',
            integrity='sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
            crossorigin='anonymous'
        ),

        script(
            src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            integrity='sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa',
            crossorigin='anonymous'
        ),

    ))

    #adicionamos um corpo ao html
    body_html = meu_html.add(body())

    #cabeçalho
    cabecalho = body_html.add(div(_class='jumbotron'))
    with cabecalho:
        h2(raw(f'Relatório de ups travadas E6000 - Nordeste <small>{data_formatada}</small>')).render()

    #adicionamos o painel de lista
    painel_das_listas = body_html.add(div(_class='panel-group', id='accordion', role='tablist', aria_multiselectable='true'))



    for cidade, cmts_lista in cmts_NE.items():
        #print(f'CIDADE: {cidade}.')

        # cabeçalho da cidade
        cabecalho_cidade = painel_das_listas.add(div(_class='panel panel-default'))
        with cabecalho_cidade:
            div(
                h4(
                    a(f'CIDADE >> {cidade.upper()}', role='button', data_toggle='collapse', data_parent='#accordion',
                      href=f'#collapse{cidade}', aria_expanded='true', aria_controls=f'collapse{cidade}',
                      _class='collapsed')
                    , _class='panel-title')
                , _class='panel-heading', role='tab', id=f'heading{cidade}')


        cabecalho_cidade_complemento = cabecalho_cidade.add(div(id=f'collapse{cidade}', _class='panel-collapse collapse', role='tabpanel', aria_labelledby=f'heading{cidade}'))  # klass='panel-collapse collapse in' para ficar aberto por padrão


        for cmts in cmts_lista:
            #print(f'CMTS: {cmts} -> Ip:{cmts_lista[cmts]}')
            ate_80, ate_90, acima_90 = pega_consumo(cmts_lista[cmts], cidade)


            #converte o dict em lista
            #cmts_lista_convertida = list(cmts_lista.keys())



            with cabecalho_cidade_complemento:

                    div(
                        div(
                            h3(f'CMTS: {cmts}'

                            ,_class='panel-title')

                        ,_class='panel-heading'),

                        div(
                            #aqui eu gero 3 divs uma para cada grau de saturação
                            div(
                                [raw(f'\n<p><a class="text-info" href="{link}" class="list-group-item list-group-item-action" target="_blank">{link}</a></p>\n') for link in ate_80]
                            ),
                            div(
                                [raw(f'\n<p><a class="text-warning" href="{link}" class="list-group-item list-group-item-action" target="_blank">{link}</a></p>\n') for link in ate_90]
                            ),
                            div(
                                [raw(f'\n<p><a class="text-danger" href="{link}" class="list-group-item list-group-item-action" target="_blank">{link}</a></p>\n') for link in acima_90]
                            )

                            , _class='panel-body')

                    ,_class='panel panel-primary')




    footer_da_pagina = body_html.add(footer(_class='page-footer font-small gray'))
    with footer_da_pagina:
        with div(_class='footer-copyright text-center py-3'):
            a('Desenvolvido por mim', href='mailto:email@me.com.br', _class='text-muted')



    #print(meu_html)

    data_formatada = data_atual.strftime('%d-%m-%Y_%H-%M-%S')
    nome_do_arquivo = path.join(path.dirname(path.realpath(__file__)), f'html_ups_NE_{data_formatada}.html')

    print('Criando o HTML...')

    #abaixo gero o arquivo e salvo em html
    try:
        with open(nome_do_arquivo, 'w') as f:
            f.write(str(meu_html))

    except IOError as Ex:
        print(f'Não foi possível gerar o arquivo! Erro: {Ex}')


    #gero um arquivo zipado já pra mandar por email
    try:
        salvando_zip = zipfile.ZipFile(f'html_ups_NE_{data_formatada}.zip', 'w')
        salvando_zip.write(f'html_ups_NE_{data_formatada}.html', compress_type=zipfile.ZIP_DEFLATED)
        salvando_zip.close()
    except IOError as Ex:
        print(f'Não foi possível gerar o arquivo .zip. Erro: {Ex}')


    print('Finalizado!')
