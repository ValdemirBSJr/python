# -*- coding: utf-8 -*-
import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    start_urls = ['https://br.udacity.com/courses/all/']

    def parse(self, response):
        divs = response.xpath("/html/body/div[1]/div/div[2]/div[2]/div[1]/div")
        #divs = response.xpath("/html/body/ir-root/ir-content/ir-course-catalog/section/div/div[2]/div[2]/div")
        for div in divs:
            link = div.xpath('.//h3/a')
            #title = link.xpath('./text()').extract_first() #pega apenas o texto da tag
            href = link.xpath('./@href').extract_first() #pega um conteudo em especifico usa arroba
            #img = div.xpath('.//img[contais(@class, "img-responsive")]/@src').extract_first() #pega imagem dentro da div que contenha a classe image responsive. Pega o source da imagem
            #description = div.xpath('.//div[2]/div[2]/text()').extract_first()

            yield scrapy.Request(

                url='https://br.udacity.com%s' % href,
                callback=self.parse_detail

            )


    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_firts()
        headline = response.xpath('//h2[contains(@class, "course-header-subtitle")]/text()').extract_first()
        image =  response.xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div[2]/div[1]/img/@src').extract_first()

        yield {

            'title': title,
            'headline' : headline,
            'image' : image

        }



            #O yield retorna uma lista a medida que for sendo requisitada. nao enche a memoria

            #pra rodar no prompt:
            #scrapy crawl udacity

            #PAra salvar num arquivo:
            #scrapy crawl udacity -o udacity_courses.json
