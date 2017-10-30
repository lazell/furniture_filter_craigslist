
# -*- coding: utf-8 -*-
"""
class FurnitureSpider(scrapy.Spider):
    name = 'furniture'
    allowed_domains = ['https://newyork.craigslist.org/d/furniture/search/fua',
                       'https://newyork.craigslist.org/d/antiques/search/ata']
    start_urls = ['https://newyork.craigslist.org/d/furniture/search/fua/',
                  'https://newyork.craigslist.org/d/antiques/search/ata']

    def parse(self, response):
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        for title in titles:
            yield {'Title': title}
"""


import scrapy
from scrapy import Request


class FurnitureSpider(scrapy.Spider):
    name = 'furniture'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/furniture/search/fua/',
                  'https://newyork.craigslist.org/d/antiques/search/ata',
                  'https://newhaven.craigslist.org/d/furniture/search/fua',
                  'https://newlondon.craigslist.org/search/fua'
                  'https://hartford.craigslist.org/search/fua',
                    ]

    data = {'Title': [], 'URL': [], 'Time' : [], 'Meta_HTML' : [], 'Section' : []}

    def parse(self, response):
        titles = response.xpath('//li[@class="result-row"]')

        for title in titles:
            image_ids = title.xpath('a/@data-ids').extract_first().strip()
            url = title.xpath('p/a/@href').extract_first().strip()
            title_ = title.xpath('p/a/text()').extract()
            timedate = title.xpath('p/time/@datetime').extract()
            meta_html = title.xpath('p/span[@class="result-meta"]').extract()[0]


            if str(response) == '<200 https://newyork.craigslist.org/d/antiques/search/ata>':
                section  = "New york - Furniture"
            elif str(response) == '<200 https://newyork.craigslist.org/d/furniture/search/fua/>':
                section = "New York - Antiques"
            else:
                section = "CT - Furniture"


            yield {'Title': title_ ,'URL': url, 'Time' : timedate, 'Meta_HTML' : meta_html, 'Section' : section, 'Image' : image_ids}



            #yield Request(url, callback=self.parse_page, meta={'URL': url,
                                                               #'Title': title_,
                                                               #'Time': timedate,
                                                               #'Meta_HTML' : meta_html,
                                                               #'Section' : section
                                                               #})

"""
    def parse_page(self, response):
        url = response.meta.get('URL')
        title_ = response.meta.get('Title')
        timedate = response.meta.get('Time')
        meta_html = response.meta.get('Meta_HTML')
        section = response.meta.get('Section')

        description = "".join(line for line in response.xpath('//*[@id="postingbody"]').extract()[0])



        yield {'URL': url,
               'Title': title_,
               'Time': timedate,
               'Meta_HTML' : meta_html,
               'Section' : section,
               'Description' : description
               'Image_URL' : image_url}


"""
