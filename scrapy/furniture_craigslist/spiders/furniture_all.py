"""import scrapy
from scrapy import Requests


class FurnitureSpider(scrapy.Spider):
    name = 'furniture'
    allowed_domains = ['https://newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/furniture/search/fua/',
                  'https://newyork.craigslist.org/d/antiques/search/ata']

    def parse(self, response):
        titles = response.xpath('//a[@class="result-info"]')

        for title in titles:
            relative_url = title.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            title_ = title.xpath('a[@class="result-title hdrlnk"]/text()'.extract_first()
            date_time = title.xpath('time[@class="result-date"]/text()'.extract_first()
            price = title.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first("")
            address = title.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")

            yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url,
                                                                        'Title': title_,
                                                                        'Address':address,
                                                                        'Date_Time': date_time,
                                                                        'Price': price,
                                                                         })

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = "https://newyork.craigslist.org" + relative_next_url

        yield Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        date_time = response.meta.get('Date_Time')
        price = response.meta.get('Price')

        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        #try alternative '//*[@id="postingbody"]/div[@class="print-information print qrcode-container"]/text()'


        yield{'URL': absolute_url,
              'Title': title_,
              'Description': description,
              'Address':address,
              'Date_Time': date_time,
              'Price': price
              }

                                                                     })
                                                                     """
