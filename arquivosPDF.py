#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Valdemir Bezerra

#como root: pip3 install PyPDF2

#esse modulo so pode ler e copiar de um pdf pra outro. nao se cria pdf do zero nem  se escreve texto livremente em um

import PyPDF2

arquivoPDFObj = open('meetingminutes.pdf', 'rb')

pdfLeitor = PyPDF2.PdfFileReader(arquivoPDFObj)

print(pdfLeitor.numPages) # numero de paginas

paginaObj = pdfLeitor.getPage(0) #pega o texto da primeira pagina

print(paginaObj.extractText())