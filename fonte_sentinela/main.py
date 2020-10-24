#!/home/PC/Documents/fonte_sentinela/venv/bin/python /home/PC/Documents/fonte_sentinela/main.py
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#imports
import re
import requests
import bs4
from os import system
from requests.auth import HTTPBasicAuth
from emoji import emojize
import telegram
from datetime import datetime
from modulos_fontes_sentinela import Lista_Site_Fontes
from modulo_shelve import Manipula_shelve, Log_errors

COMPLEMENTO_CAMINHO = 'LINK_TO_COMPLETE'
COMPLEMENTO_DETALHADO_FONTES = 'DETAILS'



def pega_detalhamento_fontes(site: str, login: str, senha: str, fontes_filtradas: list):

    retorna_fontes = ''

    for fonte in fontes_filtradas:

        #print(fonte)
        fonte_detalhada = site + COMPLEMENTO_DETALHADO_FONTES + str(fonte)
        resquest_fonte_detalhada = requests.get(fonte_detalhada, auth=HTTPBasicAuth(login, senha))
        resquest_fonte_detalhada.raise_for_status()

        pega_fonte_detalhada = bs4.BeautifulSoup(resquest_fonte_detalhada.text, 'html.parser')

        # pega o valor caso haja algum erro
        fonte_validada = pega_fonte_detalhada.find('div', attrs={'class': 'errorMessage'})

        if resquest_fonte_detalhada.status_code == 200 and fonte_validada == None:
            try:


                status_fonte_down = pega_fonte_detalhada.find('div', attrs={'class': 'hostDOWN'})

                up_since = pega_fonte_detalhada.find(string=re.compile('\(for*'))
                address_font = pega_fonte_detalhada.find('div', attrs={'class': 'dataTitle'})

                #pega a notifications. Se ela nao existir, retorna None
                notifications = pega_fonte_detalhada.find('div', attrs={'class': 'notificationsDISABLED'})
                #print(notifications)

                time_out = up_since[5:-1]
                time_out = time_out.split(' ')

                time_out = filter(None, time_out) #retiro todos os vazios

                time_out = list(time_out) #converto para lista novamente


                minutes_out = time_out[2][:-1]
                hour_out = time_out[1][:-1]
                days_out = time_out[0][:-1]

                time_format_now = datetime.now()
                time_format_out = str(time_format_now.year) + '-' + str(time_format_now.month) + '-' + str(time_format_now.day) + ' ' + hour_out + ':' + minutes_out
                time_format_out = datetime.strptime(time_format_out, '%Y-%m-%d %H:%M')

                time_out_total = abs((time_format_out - time_format_now).total_seconds())
                time_out_total = (time_out_total/60)/60 #pega a quantidade de minutos. Se for maior que 3 vai
                #print(time_out_total)

                address_font = str(address_font.getText())
                address_font = address_font.split('|')
                fonte_nome = address_font[0].strip()
                fonte_mac = address_font[1].strip()
                address_font = address_font[2].strip()


                if status_fonte_down == None and notifications != 'DISABLED' and days_out != '0':
                    #Se a notificatios existir e estiver como DISABLED, ignora a fonte

                    pass

                if status_fonte_down != None and notifications == None and time_out_total >= 3 and days_out == '0':
                    #se for maior ou 3 e nao tiver mais de um dia fora
                    #print(time_out_total)
                    retorna_fontes = retorna_fontes + str(fonte_nome) + ' - ' + str(fonte_mac) + '\n<b>Status: ' + str(status_fonte_down.getText()) + '</b>' + emojize(':red_circle:',use_aliases=True) + '\nDesde:' + str(up_since[5:-1]) + '\n' + str(address_font) + '\n\n'



            except Exception as Ex:
                retorna_fontes = 'Ops! Não foi possível retornar uma consulta no momento. Verifique se a página fontes está funcionando...'
                print(Ex)
                salva_log = Log_errors(tipo=__file__, erro=Ex)
                salva_log.registra_log()
                return retorna_fontes

    return retorna_fontes







def percorre_site_fontes(lista_site: dict):

    '''
    Entro na página e recolho só o link das fontes que estão fora.
    Status statusHOSTDOWN
    :return: link das fontes
    '''

    retorna_fontes = '\n-----------------------------------------\n'


    #print(lista_site)

    for operacao, site in lista_site.items():

        retorno_do_shelve = Manipula_shelve()
        retorno_acesso = retorno_do_shelve.mostra_shelve(operacao)
        retorno_acesso = retorno_acesso.split(',')



        #retorna_fontes = f'OPERAÇÃO: {operacao}\n\n\n'


        pagina_font = site + COMPLEMENTO_CAMINHO

        request_fonts = requests.get(pagina_font, auth=HTTPBasicAuth(retorno_acesso[1], retorno_acesso[2]))
        request_fonts.raise_for_status()
        pega_soup_fonts = bs4.BeautifulSoup(request_fonts.text, 'html.parser')

        font_fora = pega_soup_fonts.find_all('td', attrs={'class': 'statusHOSTDOWN'})


        if request_fonts.status_code == 200 and font_fora != None:

            fontes = []  # percorro a lista de links e salvo o href de cada fonte
            for fonte in font_fora:
                pega_link_fonte = fonte.find('a')
                fontes.append(pega_link_fonte.get('href'))

            fontes_filtradas = list(set(fontes))  # Cada td tem 2 links, aqui eu filtro para excluir os repetidos

            #print(fontes_filtradas)

            #pegamos o detalhado de todas as fontes
            retorno_de_fontes = pega_detalhamento_fontes(site, str(retorno_acesso[1]), str(retorno_acesso[2]), fontes_filtradas)

            #Abaixo, se o retorno não for vazio eu concateno a string com todas as fontes
            if retorno_de_fontes != None:
                retorna_fontes = retorna_fontes + retorno_de_fontes
                #print(retorna_fontes)



    #print('+' * 100)
    #print(retorna_fontes)
    return retorna_fontes





if __name__ == '__main__':



    lista = {
        'CITY': 'http://path.site.com/',

    }

    listar_site_fontes = Lista_Site_Fontes()
    listar_site_fontes.popular(lista)


    fontes_fora = percorre_site_fontes(listar_site_fontes)

    if fontes_fora =='None':
        print('Sem fontes fora no momento. Saindo...')
        exit()

    # se o retorno nao for vazio, manda mensagem. Caso nao tenha fonte fora(string vazia ou só o nome da cidade) nao faz nada
    elif fontes_fora != '' and len(fontes_fora) != 43:

        # telegram info's
        telegram_token = 'ID_BOT'
        chat_id = '-ID_CHAT'

        # cria o objeto bot para mandar as fontes
        bot = telegram.Bot(token=telegram_token)

        bot.sendMessage(chat_id=chat_id, text=fontes_fora, parse_mode='HTML')

        #print(fontes_fora)



        #Enviando como notificação do linux
        #system(f'notify-send "{fontes_fora}" -u critical')
