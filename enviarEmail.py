#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

import smtplib

teste = 'Subject: Apenas testando python rsrsrs...\nMandando email com python!!!' + 'HAAAAA'

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

print(smtpObj.ehlo()) #resposta do server

print(smtpObj.starttls()) #status do TLS

print(smtpObj.login('datacenter.jpa@gmail.com', 'emailenvioautomatico')) #login

print('Mandando email...')

smtpObj.sendmail('datacenter.jpa@gmail.com', ['valdemir.junior2@net.com.br', 'datacenter.jpa@net.com.br'], teste)

print(smtpObj.quit()) #desconecta do servidor SMTP