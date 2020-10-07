#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#imports
import re
import subprocess
import csv
import requests
import bs4
from requests.auth import HTTPBasicAuth
from emoji import emojize
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, core


def return_CMTS_name(ip_cmts):
    # All cmts to use
    list_All_CMTS = {'127.0.192.8': 'HOST01', }

    if ip_cmts == ' ':
        return 'CMTS-EMPTY'

    else:
        #search the ip on dictionary and return cmts name
        return list_All_CMTS.get(ip_cmts.strip(), 'CMTS-UNK')



def consult_ldap(client):

    server = Server('127.0.0.111', get_info=ALL)  # create info of LDAP Server

    try:

        contr = client

        conn = Connection(server, 'uid=user_root,dc=packgate,dc=packgate_docsis',
                          'SENHAA')  # mount the machine access
        # Init Bind to server
        conn.bind()
        # Search in ldap database
        conn.search('dc=packgate_docsis', f'(&(docsiscontrato={client})(docsisclientclass=classOfcliienta))',
                    attributes=['docsisclientclass', 'docsismodemmacaddress', 'docsispolicyname', 'docsiscontrato'])

        if len(conn.entries) != 0:

            ret_client = conn.entries[0]
            ret_client = str(ret_client)
            ret_client = ret_client.split(' ')
            profile = ret_client[32]
            # ret_client = (ret_client[22], ret_client[27], ret_client[32])
            # ret_client = ' | '.join(ret_client)
            ret_client = ret_client[27]
            ret_client = ret_client.split(',')
            ret_client = ret_client[2]
            ret_client = ''.join(ret_client).replace(':', '').split()  # delete the ':'
            ret_client = str(ret_client[0])
            ret_client = 'http://pagina-de-consulta.com.br/cable/cable_docsis.php?strHost=S&mac5=' + ret_client[0:2] + '&mac4=' + ret_client[2:4] + '&mac3=' + ret_client[4:6] + '&mac2=' + ret_client[6:8] + '&mac1=' + ret_client[8:10] + '&mac=' + ret_client[10:12] + ';' + contr + ';' + profile

            return ret_client

        else:
            # Imprime o que retornou
            ret_client = f'Não foi possível localizar esse contrato na base!\nContrato: {client}.'
            return ret_client


    except (core.exceptions.LDAPBindError, IndexError) as e:
        # Se a ligação ao LDAP falhar sobe esse erro
        print(f'Ligação ao LDAP falhou: {e}')
        ret_client = 'Oops! Estamos com problemas técnicos. \nTente novamente mais tarde ou consulte direto na página DTC.'
        return ret_client





def return_node_client(cmts, interface, len_inter=None):

    node = subprocess.getoutput(f'cat /home/user/Documentos/SCRIPTS/pegaSNR/interface/TODOS.txt | grep {interface} | grep {cmts}')
    node = node.split(' ')
    node = node[0]
    node = node.split('.')
    node = node[1].strip()

    if len_inter == 3: #if cmts is C4, get the correct interface
        node = int(node) - 1

    node = subprocess.getoutput(f'cat /home/user/Documentos/SCRIPTS/pegaSNR/repo/TODOS.txt | grep {node} | grep {cmts}')
    node = node.split(' ')
    node = node[3]
    node = node.split(';')
    node = node[0].strip()

    return node




def return_client(data):

    ret_client=''
    contr = ''
    profile = ''

    client = data
    client = client.strip()

    client = client[4::]

    if len(client) < 4 or len(client) > 12:

        ret_client = f'Você digitou: \"{client}\".\nContrato ou MAC digitado é inválido!\nVerifique o valor digitado!'

    else:
        if client.isdigit():

            ret_client = consult_ldap(client)


        else:

            ret_client = 'http://pagina-de-consulta.com.br/cable/cable_docsis.php?strHost=S&mac5=' + client[0:2] + '&mac4=' + client[2:4] + '&mac3=' + client[4:6] + '&mac2=' + client[6:8] + '&mac1=' + client[8:10] + '&mac=' + client[10:12]

            request_page = requests.get(ret_client, auth=HTTPBasicAuth('login', 'senha'))

            request_page.raise_for_status()

            transform_soup = bs4.BeautifulSoup(request_page.text, 'html.parser')

            element_page = transform_soup.select('td')

            if request_page.status_code == 200:

                try:

                    vendor_cmts = element_page[9].getText().split(' ')
                    vendor_cmts = vendor_cmts[2][0:5]

                    if vendor_cmts == 'Arris':
                        contract = element_page[16].getText().split(' ')
                        contract = contract[2].strip()
                        profile = transform_soup.find(string=re.compile('Profile:')) #get tag by text
                        profile = profile.find_next('td').getText().strip()

                    if vendor_cmts == 'Cisco':
                        contract = element_page[18].getText().split(' ')
                        contract = contract[2].strip()
                        profile = transform_soup.find(string=re.compile('Profile:')) #get tag by text
                        profile = profile.find_next('td').getText().strip()

                    #print(profile)
                    ret_client = ret_client + ';' + contract + ';' + profile

                except IndexError as e:
                    print(f'Tivemos um erro! {e}')
                    ret_client = 'Oops, não foi possível localizar um cable.\nVerifique se o MAC está correto.'


    if ret_client[0:4] == 'http':

        ret_client = ret_client.split(';')

        contr = ret_client[1]
        profile = ret_client[2]
        ret_client = ret_client[0]




        request_page = requests.get(ret_client, auth=HTTPBasicAuth('login', 'senha'))

        request_page.raise_for_status()

        transform_soup = bs4.BeautifulSoup(request_page.text, 'html.parser')

        element_page = transform_soup.select('td')


        if request_page.status_code == 200:

            try:

                vendor_cmts = element_page[9].getText().split(' ')
                vendor_cmts = vendor_cmts[2][0:5]

                if vendor_cmts == 'Arris':

                    cmts = element_page[7].getText().split(' ')
                    cmts = cmts[2].strip()
                    cmts_ip = element_page[7].getText().split(' ')
                    cmts_ip = cmts_ip[1].strip()
                    interface = element_page[8].getText().split(' ')
                    len_inter = len(interface)
                    interface = interface[-1].strip() #get the last item: 3 for C4 or 4 for E6k
                    ip = element_page[18].getText().split(' ')
                    ip = ip[6].strip()
                    ip_mib = subprocess.getoutput('snmpgetnext -v2c -c public ' + ip + ' .1.3.6.1.2.1.4.20.1.1.127.0.0.1')
                    ip_mib = ip_mib.split(' ')
                    ip_cpe = ip_mib[3].strip()
                    tx = element_page[25].getText().split(' ')
                    tx = tx[0].strip()
                    rx = element_page[27].getText().split(' ')
                    rx = rx[0].strip()
                    snr = element_page[29].getText().split(' ')
                    snr = snr[0].strip()
                    status = element_page[11].getText().strip()

                    node_info = return_node_client(cmts_ip, interface, len_inter)

                    ret_client = f'CMTS: {cmts} | UP: {interface}\n{status} | Node: {node_info}\nCable IP: {ip} | IP CPE: {ip_cpe}\nTX: {tx} | RX: {rx} | SNR: {snr}\nContrato: {contr} | Profile: {profile}' #+ '\n------------------\n' + node_info

                if vendor_cmts == 'Cisco':

                    cmts = element_page[7].getText().split(' ')
                    cmts = cmts[2].strip()
                    cmts_ip = element_page[7].getText().split(' ')
                    cmts_ip = cmts_ip[1].strip()
                    interface = element_page[8].getText().split(' ')
                    interface = interface[1].strip()
                    ip = element_page[20].getText().split(' ')
                    ip = ip[6].strip()
                    ip_mib = subprocess.getoutput('snmpgetnext -v2c -c public ' + ip + ' .1.3.6.1.2.1.4.20.1.1.127.0.0.1')
                    ip_mib = ip_mib.split(' ')
                    ip_cpe = ip_mib[3].strip()
                    tx = element_page[27].getText().split(' ')
                    tx = tx[0].strip()
                    rx = element_page[29].getText().split(' ')
                    rx = rx[0].strip()
                    snr = element_page[31].getText().split(' ')
                    snr = snr[0].strip()
                    status = element_page[11].getText().strip()

                    node_info = return_node_client(cmts_ip, interface)

                    ret_client = f'CMTS: {cmts} | UP: {interface}\n{status} | Node: {node_info}\nCable IP: {ip} | IP CPE: {ip_cpe}\nTX: {tx} | RX: {rx} | SNR: {snr}\nContrato: {contr} | Profile: {profile}' #+ '\n------------------\n' + node_info




            except IndexError as e:
                print(f'Tivemos um erro! {e}')
                ret_client = 'Oops, não foi possível localizar um cable.\nCable pode estar offline a tempos.'




            finally:

                return ret_client


    else:
        print('Parou aqui mesmo. retorna apenas o link.')
        return ret_client



def return_font(font):

    #get the info for search the font

    font = font.strip()

    data_font = font[6::].upper()
    data_font = data_font.replace(' ', '')
    get_font = ''

    if len(data_font) < 4 or len(data_font) > 8:
        get_font = 'Você digitou: \"'+ str(data_font) + '\".\nvalor digitado é muito curto ou muito longo para ser de uma fonte válida.'

    else:
        #mount the csv data's in dictionary, after search the csv data for de taped value
        with open('/home/user/Documentos/SCRIPTS/cibillaSNR/fontes.csv', 'r') as archive:

            reader = csv.reader(archive)

            dataAllFonts = {}
            for row in reader:
                key = row[0]
                if key not in dataAllFonts:
                    dataAllFonts[key] = str(row[1]) + ';' + str(row[2])


        for key, value in dataAllFonts.items():
            if key.startswith(data_font):
                #print(key, value)

                value = str(value)
                value = value.split(';')
                value_mac = value[0]
                value_type = str(value[1]) + '_'


                page_fonts = 'http://127.0.0.25/nagios_fontes/cgi-bin/extinfo.cgi?type=1&host=' + str(value_type) + str(value_mac)

                #print(page_fonts)

                request_fonts = requests.get(page_fonts, auth=HTTPBasicAuth('login', 'senha'))

                request_fonts.raise_for_status()

                get_soup_fonts = bs4.BeautifulSoup(request_fonts.text, 'html.parser')

                font_valid = get_soup_fonts.find('div', attrs={'class': 'errorMessage'})
                #print(font_valid)


                if request_fonts.status_code == 200 and font_valid == None:

                    try:

                        status_font = get_soup_fonts.find('div', attrs={'class': 'hostUP'})
                        status_font_down = get_soup_fonts.find('div', attrs={'class': 'hostDOWN'})
                        up_since = get_soup_fonts.find(string=re.compile('\(for*'))
                        address_font = get_soup_fonts.find('div', attrs={'class': 'dataTitle'})

                        address_font = str(address_font.getText())
                        address_font = address_font.split('|')
                        address_font = address_font[2].strip()

                        if status_font != None:

                            get_font = get_font + str(key) + ' - MAC: ' + str(value_mac) + '\n<strong>Status: ' + str(status_font.getText()) + '</strong> ' + emojize(':large_blue_circle:', use_aliases=True) + '\nDesde:'+ str(up_since[5:-1]) + '\n' + str(address_font) + '\n'

                        if status_font_down != None:

                            get_font = get_font + str(key) + ' - MAC: ' + str(value_mac) + '\n<strong>Status: ' + str(status_font_down.getText()) + '</strong> ' + emojize(':red_circle:', use_aliases=True) + '\nDesde:' + str(up_since[5:-1]) + '\n' + str(address_font) + '\n'

                    except:
                        get_font = 'Oops! Alguns valores não puderam ser retornados ou fonte inexistente. Valor buscado: ' +str(data_font)

                else:

                    get_font = 'Oops. Serviço nagios fontes pode estar fora.\nNão conseguimos achar uma fonte com estes parâmetros: ' + str(data_font)





    return get_font




def return_node(node):

    #get the node info for search in database the info for mibs

    node = node.strip()
    get_nodes = ''
    data_node = node[5::].upper()
    data_node = data_node.replace(' ', '')

    if data_node.isdigit():
        get_nodes = 'Nenhum node tem valor puramente numérico.'

    if len(data_node) < 4 or len(data_node) > 8 or data_node == 'VAZIO' or data_node == 'LIVRE':
        get_nodes = 'Você digitou: \"' + str(data_node) + '\".\nValor digitado é muito curto ou muito longo para ser de um node.'

    else:

        get_nodes = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/pegaSNR/repo/TODOS.txt | grep ' + data_node)

        if len(get_nodes) == 0:
            get_nodes = 'Não encontramos nenhum node com esse parâmetro'

        else:

            get_data = get_nodes.split('\n')


            #clear to variable for reuse
            get_nodes = ' '

            for data in range(len(get_data)):
                get_cmts = get_data[data].split(';')
                get_cmts = get_cmts[1].strip()


                get_node_description = get_data[data].split(' ')
                get_node_description = get_node_description[3].split(';')
                get_node_description = get_node_description[0].strip()

                get_ifAlias_node = get_data[data].split('.')
                get_ifAlias_node = get_ifAlias_node[1].split(' ')
                get_ifAlias_node = get_ifAlias_node[0].strip()


                #print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node))

                if get_cmts != ' ' and get_node_description != ' ' and get_ifAlias_node != ' ':

                    get_vendor_CMTS = subprocess.getoutput('snmpget -v2c -c  public ' + get_cmts + ' SNMPv2-MIB::sysDescr.0')
                    #print(get_vendor_CMTS[0:51:])



                    if get_ifAlias_node.isdigit() and get_vendor_CMTS[0:51:] == 'SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software':
                        #CISCO

                        get_SNR = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.5.' + get_ifAlias_node)
                        get_SNR = get_SNR.split(' ')
                        get_SNR = get_SNR[3].strip()

                        if get_SNR.isdigit() and float(get_SNR) >= 0:

                            get_interface = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' IF-MIB::ifDescr.' + get_ifAlias_node)
                            get_interface = get_interface.split(' ')
                            get_interface = get_interface[3].strip()

                            get_Cables = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.9.9.116.1.4.1.1.5.' + get_ifAlias_node)
                            get_Cables = get_Cables.split(' ')
                            get_Cables = get_Cables[3].strip()

                            get_Cables_registered = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.9.9.116.1.4.1.1.3.' + get_ifAlias_node)
                            get_Cables_registered = get_Cables_registered.split(' ') #get total cables actualy
                            get_Cables_registered = get_Cables_registered[3].strip()

                            name_cmts = return_CMTS_name(get_cmts)

                            get_SNR = float(get_SNR) * 0.1

                            #get trafic, fec and fecNc on the TODOS.txt. get it's diarily
                            get_Unecor_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.2.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_Unecor_old = get_Unecor_old.split(';')
                            get_Unecor_old = get_Unecor_old[0]
                            get_Unecor_old = get_Unecor_old.split(' ')
                            get_Unecor_old = get_Unecor_old[3].strip()
                            #print(get_Unecor_old)

                            get_fec_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.3.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_fec_old = get_fec_old.split(';')
                            get_fec_old = get_fec_old[0]
                            get_fec_old = get_fec_old.split(' ')
                            get_fec_old = get_fec_old[3].strip()
                            #print(get_fec_old)

                            get_fecN_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.4.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_fecN_old = get_fecN_old.split(';')
                            get_fecN_old = get_fecN_old[0]
                            get_fecN_old = get_fecN_old.split(' ')
                            get_fecN_old = get_fecN_old[3].strip()
                            #print(get_fecN_old)

                            get_Unecor_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.2.' + get_ifAlias_node)
                            get_Unecor_new = get_Unecor_new.split(' ')
                            get_Unecor_new = get_Unecor_new[3].strip()

                            get_fec_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.3.' + get_ifAlias_node)
                            get_fec_new = get_fec_new.split(' ')
                            get_fec_new = get_fec_new[3].strip()

                            get_fecN_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.4.' + get_ifAlias_node)
                            get_fecN_new = get_fecN_new.split(' ')
                            get_fecN_new = get_fecN_new[3].strip()


                            # get the emoji correctly for SNR number
                            if get_SNR <= 29:
                                emoji = emojize(':red_circle:', use_aliases=True)
                            else:
                                emoji = emojize(':large_blue_circle:', use_aliases=True)



                            #if Unecor is don't calculate, set the values with errors. then treats if there is any invalid value
                            if (get_Unecor_old.isdigit() and float(get_Unecor_old) > 0) and (get_Unecor_new.isdigit() and float(get_Unecor_new) > 0):
                                if (get_fec_old.isdigit() and float(get_fec_old) > 0) and (get_fec_new.isdigit() and float(get_fec_new) > 0) and (get_fecN_old.isdigit() and float(get_fecN_old) > 0) and (get_fecN_new.isdigit() and float(get_fecN_new) > 0):



                                    try:

                                        get_fec = (float(get_fec_new) - float(get_fec_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100
                                        get_fecN = (float(get_fecN_new) - float(get_fecN_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100

                                    except ZeroDivisionError:
                                        get_fec = 0
                                        get_fecN = 0

                                    finally:

                                        # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                        get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong> '+ emoji +' FC: ' + str(round(float(get_fec), 2)) + '% FN: ' + str(round(float(get_fecN), 2)) + '%' + '\n'



                                else:
                                    get_fec = 'ERFECZ'
                                    get_fecN = 'ERFECZ'

                                    emoji = emojize(':warning:', use_aliases=True)

                                    # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                    get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong> '+ emoji +' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'



                            else:
                                get_fec = 'ERUNECOR'
                                get_fecN = 'ERUNECOR'

                                emoji = emojize(':no_entry_sign:', use_aliases=True)

                                # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong>  '+ emoji +' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'




                    if get_ifAlias_node.isdigit() and get_vendor_CMTS == 'SNMPv2-MIB::sysDescr.0 = STRING: CMTS_V08.03.01.04, <<HW_REV: 3.0; VENDOR: ARRIS; BOOTR: V00.01.00>>':
                        #C4
                        ifAlias_Arris = int(get_ifAlias_node) + 1

                        get_SNR = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.5.' + str(ifAlias_Arris))
                        get_SNR = get_SNR.split(' ')
                        get_SNR = get_SNR[3].strip()

                        if get_SNR.isdigit() and float(get_SNR) >= 0:

                            name_cmts = return_CMTS_name(get_cmts)

                            get_interface = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' IF-MIB::ifDescr.' + str(ifAlias_Arris))
                            get_interface = get_interface.split(' ')
                            get_interface = get_interface[4].strip()

                            get_Cables_Ind = subprocess.getoutput('snmpwalk -v2c -c public ' + get_cmts + ' IF-MIB::ifStackStatus | grep ' + str(get_ifAlias_node))
                            get_Cables_Ind = get_Cables_Ind.split('\n')
                            get_Cables_Ind = get_Cables_Ind [-1] #get las value of list
                            get_Cables_Ind = get_Cables_Ind.split('.')
                            get_Cables_Ind = get_Cables_Ind[1]
                            #print(get_Cables_Ind)

                            get_Cables_registered = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.4998.1.1.20.2.27.1.17.' + str(get_Cables_Ind) + '.' + str(ifAlias_Arris))
                            get_Cables_registered = get_Cables_registered.split(' ')
                            get_Cables_registered = get_Cables_registered[3].strip()

                            get_Cables = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.4998.1.1.20.2.27.1.13.' + str(get_Cables_Ind) + '.' + str(ifAlias_Arris))
                            get_Cables = get_Cables.split(' ')
                            get_Cables = get_Cables[3].strip()



                            get_SNR = float(get_SNR) * 0.1


                            #get trafic, fec and fecNc on the TODOS.txt. get it's diarily
                            get_Unecor_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.2.' + str(ifAlias_Arris) + ' | grep ' + get_cmts)
                            get_Unecor_old = get_Unecor_old.split(';')
                            get_Unecor_old = get_Unecor_old[0]
                            get_Unecor_old = get_Unecor_old.split(' ')
                            get_Unecor_old = get_Unecor_old[3].strip()
                            #print(get_Unecor_old)

                            get_fec_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.3.' + str(ifAlias_Arris) + ' | grep ' + get_cmts)
                            get_fec_old = get_fec_old.split(';')
                            get_fec_old = get_fec_old[0]
                            get_fec_old = get_fec_old.split(' ')
                            get_fec_old = get_fec_old[3].strip()
                            #print(get_fec_old)

                            get_fecN_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.4.' + str(ifAlias_Arris) + ' | grep ' + get_cmts)
                            get_fecN_old = get_fecN_old.split(';')
                            get_fecN_old = get_fecN_old[0]
                            get_fecN_old = get_fecN_old.split(' ')
                            get_fecN_old = get_fecN_old[3].strip()
                            #print(get_fecN_old)

                            get_Unecor_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.2.' + str(ifAlias_Arris))
                            get_Unecor_new = get_Unecor_new.split(' ')
                            get_Unecor_new = get_Unecor_new[3].strip()

                            get_fec_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.3.' + str(ifAlias_Arris))
                            get_fec_new = get_fec_new.split(' ')
                            get_fec_new = get_fec_new[3].strip()

                            get_fecN_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.4.' + str(ifAlias_Arris))
                            get_fecN_new = get_fecN_new.split(' ')
                            get_fecN_new = get_fecN_new[3].strip()

                            # get the emoji correctly for SNR number
                            if get_SNR <= 29:
                                emoji = emojize(':red_circle:', use_aliases=True)
                            else:
                                emoji = emojize(':large_blue_circle:', use_aliases=True)


                            #if Unecor is don't calculate, set the values with errors. then treats if there is any invalid value
                            if (get_Unecor_old.isdigit() and float(get_Unecor_old) > 0) and (get_Unecor_new.isdigit() and float(get_Unecor_new) > 0):
                                if (get_fec_old.isdigit() and float(get_fec_old) > 0) and (get_fec_new.isdigit() and float(get_fec_new) > 0) and (get_fecN_old.isdigit() and float(get_fecN_old) > 0) and (get_fecN_new.isdigit() and float(get_fecN_new) > 0):

                                    try:

                                        get_fec = (float(get_fec_new) - float(get_fec_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100
                                        get_fecN = (float(get_fecN_new) - float(get_fecN_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100

                                    except ZeroDivisionError:
                                        get_fec = 0
                                        get_fecN = 0

                                    finally:
                                        # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                        get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong> ' + emoji + ' FC: ' + str(round(float(get_fec), 2)) + '% FN: ' + str(round(float(get_fecN), 2)) + '%' + '\n'



                                else:
                                    get_fec = 'ERFECZ'
                                    get_fecN = 'ERFECZ'

                                    emoji = emojize(':warning:', use_aliases=True)

                                    # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                    get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong>  '+emoji +' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'



                            else:
                                get_fec = 'ERUNECOR'
                                get_fecN = 'ERUNECOR'

                                emoji = emojize(':no_entry_sign:', use_aliases=True)

                                # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong>  ' + emoji + ' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'










                    if get_ifAlias_node.isdigit() and get_vendor_CMTS == 'SNMPv2-MIB::sysDescr.0 = STRING: CER_V06.05.00.0059, <<HW_REV: 4.0; VENDOR: ARRIS; BOOTR: V00.01.00>>':
                        #E6000

                        get_SNR = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.5.' + get_ifAlias_node)
                        get_SNR = get_SNR.split(' ')
                        get_SNR = get_SNR[3].strip()

                        if get_SNR.isdigit() and float(get_SNR) >= 0:

                            name_cmts = return_CMTS_name(get_cmts)

                            ifAlias_E6k = int(get_ifAlias_node) - 1

                            get_interface = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' IF-MIB::ifDescr.' + str(get_ifAlias_node))
                            get_interface = get_interface.split(' ')
                            get_interface = get_interface[5].strip()

                            get_Cables_Ind = subprocess.getoutput('snmpwalk -v2c -c public ' + get_cmts + ' IF-MIB::ifStackStatus | grep ' + str(ifAlias_E6k))
                            get_Cables_Ind = get_Cables_Ind.split('\n')
                            get_Cables_Ind = get_Cables_Ind [-1] #get las value of list
                            get_Cables_Ind = get_Cables_Ind.split('.')
                            get_Cables_Ind = get_Cables_Ind[1]

                            get_Cables_registered = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.4998.1.1.20.2.27.1.17.' + str(get_Cables_Ind) + '.' + str(get_ifAlias_node))
                            get_Cables_registered = get_Cables_registered.split(' ')
                            get_Cables_registered = get_Cables_registered[3].strip()

                            get_Cables = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::enterprises.4998.1.1.20.2.27.1.13.' + str(get_Cables_Ind) + '.' + str(get_ifAlias_node))
                            get_Cables = get_Cables.split(' ')
                            get_Cables = get_Cables[3].strip()


                            get_SNR = float(get_SNR) * 0.1


                            #get trafic, fec and fecNc on the TODOS.txt. get it's diarily
                            get_Unecor_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.2.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_Unecor_old = get_Unecor_old.split(';')
                            get_Unecor_old = get_Unecor_old[0]
                            get_Unecor_old = get_Unecor_old.split(' ')
                            get_Unecor_old = get_Unecor_old[3].strip()
                            #print(get_Unecor_old)

                            get_fec_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.3.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_fec_old = get_fec_old.split(';')
                            get_fec_old = get_fec_old[0]
                            get_fec_old = get_fec_old.split(' ')
                            get_fec_old = get_fec_old[3].strip()
                            #print(get_fec_old)

                            get_fecN_old = subprocess.getoutput('cat /home/user/Documentos/SCRIPTS/cibillaSNR/dirNode/TODOS.txt | grep SNMPv2-SMI::transmission.127.1.1.4.1.4.' + get_ifAlias_node + ' | grep ' + get_cmts)
                            get_fecN_old = get_fecN_old.split(';')
                            get_fecN_old = get_fecN_old[0]
                            get_fecN_old = get_fecN_old.split(' ')
                            get_fecN_old = get_fecN_old[3].strip()
                            #print(get_fecN_old)

                            get_Unecor_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.2.' + get_ifAlias_node)
                            get_Unecor_new = get_Unecor_new.split(' ')
                            get_Unecor_new = get_Unecor_new[3].strip()

                            get_fec_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.3.' + get_ifAlias_node)
                            get_fec_new = get_fec_new.split(' ')
                            get_fec_new = get_fec_new[3].strip()

                            get_fecN_new = subprocess.getoutput('snmpget -v2c -c public ' + get_cmts + ' SNMPv2-SMI::transmission.127.1.1.4.1.4.' + get_ifAlias_node)
                            get_fecN_new = get_fecN_new.split(' ')
                            get_fecN_new = get_fecN_new[3].strip()

                            # get the emoji correctly for SNR number
                            if get_SNR <= 29:
                                emoji = emojize(':red_circle:', use_aliases=True)
                            else:
                                emoji = emojize(':large_blue_circle:', use_aliases=True)


                            #if Unecor is don't calculate, set the values with errors. then treats if there is any invalid value
                            if (get_Unecor_old.isdigit() and float(get_Unecor_old) > 0) and (get_Unecor_new.isdigit() and float(get_Unecor_new) > 0):
                                if (get_fec_old.isdigit() and float(get_fec_old) > 0) and (get_fec_new.isdigit() and float(get_fec_new) > 0) and (get_fecN_old.isdigit() and float(get_fecN_old) > 0) and (get_fecN_new.isdigit() and float(get_fecN_new) > 0):

                                    try:

                                        get_fec = (float(get_fec_new) - float(get_fec_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100
                                        get_fecN = (float(get_fecN_new) - float(get_fecN_old)) / ((float(get_Unecor_new) - float(get_Unecor_old)) + (float(get_fec_new) - float(get_fec_old)) + (float(get_fecN_new) - float(get_fecN_old))) * 100
                                    except ZeroDivisionError:
                                        get_fec = 0
                                        get_fecN = 0
                                    finally:
                                        # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                        get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong> ' + emoji + ' FC: ' + str(round(float(get_fec), 2)) + '% FN: ' + str(round(float(get_fecN), 2)) + '%' + '\n'



                                else:
                                    get_fec = 'ERFECZ'
                                    get_fecN = 'ERFECZ'

                                    emoji = emojize(':warning:', use_aliases=True)

                                    # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                    get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong>  ' + emoji + ' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'



                            else:
                                get_fec = 'ERUNECOR'
                                get_fecN = 'ERUNECOR'

                                emoji = emojize(':no_entry_sign:', use_aliases=True)

                                # print('CMTS: ' + str(get_cmts) + ' Node: ' + str(get_node_description) + ' ALIAS: ' + str(get_ifAlias_node) + ' Interface: ' + str(get_interface) + ' Qtde.: ' + str(get_Cables) + ' SNR: ' +str(round(get_SNR, 2)))
                                get_nodes = get_nodes + str(name_cmts) + ' N: ' + str(get_node_description) + ' In: ' + str(get_interface) + ' TE: ' + str(get_Cables_registered) + '/' + str(get_Cables) + ' <strong>SNR: ' + str(round(float(get_SNR), 2)) + '</strong>  ' + emoji + ' FC: ' + str(get_fec) + '% FN: ' + str(get_fecN) + '%' + '\n'





    return get_nodes




def get_soup_ofensors(link_ofensors):

    requests_ofensors = requests.get(link_ofensors, auth=HTTPBasicAuth('gerenciaJPA', '@ust1n'))

    get_soup_ofensors = bs4.BeautifulSoup(requests_ofensors.text, 'html.parser')

    ofensors = get_soup_ofensors.find_all('td', attrs={'class': 'statusBGCRITICAL'})

    return_str_ofensors = ' '

    for ofensor in range(0, len(ofensors)):

        if ofensors[ofensor].getText()[0:4] == 'Node':

            return_str_ofensors = return_str_ofensors + ofensors[ofensor].getText() + '\n'


    return return_str_ofensors


def return_ofensors(message):
    get_ofensors = get_soup_ofensors('http://127.0.0.18/nagios_slave3/cgi-bin/status.cgi?host=all&servicestatustypes=16&hoststatustypes=15')
    get_ofensors = get_ofensors + get_soup_ofensors('http://127.0.0.18/nagios_slave1/cgi-bin/status.cgi?host=all&servicestatustypes=16&hoststatustypes=15')
    get_ofensors = get_ofensors + get_soup_ofensors('http://127.0.0.18/nagios_slave2/cgi-bin/status.cgi?host=all&servicestatustypes=16&hoststatustypes=15')


    return get_ofensors










if __name__ == '__main__':
    pass



