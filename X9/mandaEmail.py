#!/home/user/.virtualenvs/k36/bin/python
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

from datetime import date


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def MandaEmail(**kwargs):


    hoje = date.today()


    mensagemMontada = MIMEMultipart()

    mensagemMontada['Subject'] = "ERRO na execucao do crontab em - " + str(hoje.day) + "/" + str(hoje.month) + "/" + str(hoje.year)

    mensagemMontada.attach(MIMEText('Prezados, o X9 identificou um erro na execução do crontab do(s) seguinte(s) arquivo(s): ' + kwargs['nome'] + '. Segue o erro: ' + kwargs['descricao']))


    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)

    print(smtpObj.ehlo())  # resposta do server

    print(smtpObj.starttls())  # status do TLS

    smtpObj.login('emaildeenvio@gmail.com', 'senhaemailenvioautomatico')  # login


    smtpObj.sendmail('emaildeenvio@gmail.com', ['email-destino1@gmail.com.br', 'emaildestino2@gmail.com.br',], mensagemMontada.as_string())

    print(smtpObj.quit())  # desconecta do servidor SMTP
