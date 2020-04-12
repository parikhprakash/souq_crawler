from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from souq.items import SouqItem
class MySpider(CrawlSpider):
    name="women_spidy"
    allowed_domains = ["saudi.souq.com"]
    start_urls = ['https://saudi.souq.com/sa-en/women/dresses-465']

    rules = (
        Rule(
            LinkExtractor(allow=('.*(man|men).*/(i|u)/')) ,callback="parse_item"),
        Rule(
            LinkExtractor(allow=('/sa-en/.*women.*')),follow=True
        ),
        
    )

    def parse_item(self,response):
        self.logger.debug("PARSING ITEM")
        item = SouqItem()
        item['product_name'] = "".join(response.xpath('//*[@id="content-body"]/div/header/div[2]/div[2]/div[2]/div[1]/div/h1/text()').extract())
        item['product_url'] = response.url
        item['product_price'] = "".join(response.xpath('//*[@id="content-body"]/div/header/div[2]/div[2]/div[3]/div/section/div/div/div[1]/h3/text()[2]').extract()).strip()
        specs = dict(zip(response.xpath('//*[@id="specs-full"]/dl/dt/text()').extract(),response.xpath('//*[@id="specs-full"]/dl/dd/text()').extract()))
        item['product_specification'] = specs
        data_description_li =  response.xpath('//*[@id="content-body"]/div/header/div[2]/div[2]/div[3]/div/div[2]/ul/li/text()').extract()
        data_description_text =  response.xpath('//*[@id="content-body"]/div/header/div[2]/div[2]/div[3]/div/div[2]/p[2]/text()').extract()
        data_description = data_description_li + data_description_text
        item['product_description'] = data_description
        item['product_images'] = response.xpath('//*[@id="content-body"]/div/header/div[2]/div[2]/div[2]/div[3]/div/div/div/a/div/img/@data-url').extract()
        yield item