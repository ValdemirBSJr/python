# -*- coding: utf-8 -*-
import scrapy

"""
IMPORTANTE: Se der erro 544 significa que o site identificou que é um robo e tá bloqueando acesso
para desbloquear va no arquivo settings.py da pasta spiders do projeto e mude o valor da linha 19 'USER AGENT'
para "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

Descomentar tambem a 67, item pipeline pra poder usar o modulo pipelines pra poder salvar no banco 'Modulo pipelines.py'
"""
class CarsSpider(scrapy.Spider):

    name = 'cars'
    allowed_domains = ['pb.olx.com.br'] #essa e a lista de dominios permitidos. Bote a root quando quer navegar entre as paginas
    start_urls = ['http://pb.olx.com.br/veiculos-e-acessorios/carros/']

    def parse(self, response):
        items = response.xpath('//ul[@id="main-ad-list"]/li[not(contains(@class, "list_native"))]') #pega todos os elementos ul de id main-ad-list dentro de li

        self.log(len(items))

        for item in items:
            self.log(item.xpath('./a/@href').extract_first())
            url = item.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

        #Apos pegar os conteudos e verifica se tem outra pagina
        next_page = response.xpath('//div[contains(@class, "module_pagination")]//a[@rel = "next"]/@href').extract_first()

        if next_page:
            self.log('Próxima página: %s' % next_page.extract_first())
            #Abaixo uso recursividade. Se tiver um next page ele executa a funcao parse de novo do começo
            #nao é bom usar por que ele vai pegar toda, pode ser bloqueado
            yield scrapy.Request(url=next_page.extract_first(), callback=self.parse)


    def parse_detail(self, response):
        #self.log(response.url)
        title = response.xpath('//title/text()').extract_first()
        year = response.xpath('//span[contains(text(), "Ano")]/following-sibling::strong/a/@title').extract_first()
        ports = response.xpath('//span[contains(text(), "Portas")]/following-sibling::strong/a/text()').extract_first()

        yield {

            'title': title,
            'year': year,
            'ports': ports,
        }
