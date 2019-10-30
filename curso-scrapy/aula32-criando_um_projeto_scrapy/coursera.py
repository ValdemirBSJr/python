# -*- coding: utf-8 -*-
import scrapy


class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    #allowed_domains = ['https://pt.coursera.org/'] #nao precisa aqui
    start_urls = ['https://pt.coursera.org//']

    def parse(self, response):
        #pass
        self.log("Hello world! scrapy project")
