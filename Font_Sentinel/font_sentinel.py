#!/home/env python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#imports
import re
import requests
import bs4
from requests.auth import HTTPBasicAuth
from emoji import emojize
import telegram
from datetime import datetime, timedelta


def verifica_fontes() -> str:

    '''
    Entro na página e recolho só o link das fontes que estão fora.
    Status statusHOSTDOWN
    :return: link das fontes
    '''


    pagina_font = 'http://path_to_FONT_NAGIOS'

    request_fonts = requests.get(pagina_font, auth=HTTPBasicAuth('LOGIN', 'PASWD'))

    request_fonts.raise_for_status()

    pega_soup_fonts = bs4.BeautifulSoup(request_fonts.text, 'html.parser')

    font_fora = pega_soup_fonts.find_all('td', attrs={'class': 'statusHOSTDOWN'})

    #print(font_fora)




    retorna_fontes = ''


    if request_fonts.status_code == 200 and font_fora != None:

        fontes = [] #percorro a lista de links e salvo o href de cada fonte
        for fonte in font_fora:
            pega_link_fonte = fonte.find('a')
            fontes.append(pega_link_fonte.get('href'))


        fontes_filtradas = list(set(fontes)) #Cada td tem 2 links, aqui eu filtro para excluir os repetidos

        #print(fontes_filtradas)

        #pegamos o detalhado de todas as fontes
        for fonte in fontes_filtradas:

            #print(fonte)

            fonte_detalhada = 'http://path_to_font_dir' + str(fonte)

            resquest_fonte_detalhada = requests.get(fonte_detalhada, auth=HTTPBasicAuth('LOGIN', 'PASSWD'))

            resquest_fonte_detalhada.raise_for_status()

            pega_fonte_detalhada = bs4.BeautifulSoup(resquest_fonte_detalhada.text, 'html.parser')

            #pega o valor caso haja algum erro
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
                    time_out_total = time_out_total/60 #pega a quantidade de minutos. Se for maior que 5 vai


                    address_font = str(address_font.getText())
                    address_font = address_font.split('|')
                    fonte_nome = address_font[0].strip()
                    fonte_mac = address_font[1].strip()
                    address_font = address_font[2].strip()

                    if status_fonte_down == None and notifications != 'DISABLED' and days_out != '0':
                        #Se a ntificatios existir e estiver como DISABLED, ignora a fonte

                        retorna_fontes = 'nada'

                    if status_fonte_down != None and notifications == None and time_out_total >= 5:

                        #print(status_fonte_down)
                        retorna_fontes = retorna_fontes + str(fonte_nome) + ' - ' + str(fonte_mac) + '\n<b>Status: ' + str(
                            status_fonte_down.getText()) + '</b>' + emojize(':red_circle:',
                                                                                 use_aliases=True) + '\nDesde:' + str(
                            up_since[5:-1]) + '\n' + str(address_font) + '\n\n'


                    return retorna_fontes


                except Exception as e:
                    retorna_fontes = 'Ops! Não foi possível retornar uma consulta no momento. Verifique se a página fontes está funcionando...'
                    print(e)
                    return retorna_fontes

    else:
        print('Sem fontes fora no momento')
        retorna_fontes = 'nada'
        return retorna_fontes


if __name__ == '__main__':

    retorno_de_fontes = verifica_fontes()
    print(retorno_de_fontes)

    if retorno_de_fontes == None:

        print('Sem fontes fora no momento...')
        exit()

    #se o retorno nao for vazio, manda mensagem. Caso nao tenha fonte fora(string vazia) nao faz nada
    if retorno_de_fontes != '':

        # telegram info's
        telegram_token = 'TOKEN'
        chat_id = '-CHAT_ID'

        # crea o objeto bot para mandar as fontes
        bot = telegram.Bot(token=telegram_token)

        bot.sendMessage(chat_id=chat_id, text=retorno_de_fontes, parse_mode='HTML')
