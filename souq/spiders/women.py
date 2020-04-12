from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from souq.items import SouqItem
import pickle
class MySpider(CrawlSpider):
    category_list =  pickle.load(open('cat.pkl','rb'))
    name="women_spidy"
    allowed_domains = ["saudi.souq.com"]
    start_urls = ['https://saudi.souq.com/sa-en/women/dresses-465',
        'https://saudi.souq.com/sa-en/women/tops-488/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/pants/pants-477/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/sportswear/sportswear-467/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/women/womens-lingerie-348/a-t/s/',
        'https://saudi.souq.com/sa-en/skirts/skirts-483/a-t/s/',
        'https://saudi.souq.com/sa-en/women/jackets---and---coats-473/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/women/ethnic---and---traditional-wear-518/a-t/s/',
        'https://saudi.souq.com/sa-en/jeans/pants-477/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/sleepwear/sleepwear-484/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/swimwear/swimwear-487/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/abaya/ethnic---and---traditional-wear-518/a-t/s/',
        'https://saudi.souq.com/sa-en/hoodies/tops-488/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/tote/handbags-472/a-t/s/',
        'https://saudi.souq.com/sa-en/bags/handbags-472/crossbody-bags/women/a-t-6328-6356/s/',
        'https://saudi.souq.com/sa-en/women/backpacks-468/a-t/s/',
        'https://saudi.souq.com/sa-en/duffle-bags/duffle-bags-559/a-t/s/',
        'https://saudi.souq.com/sa-en/women/wallets-533/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/women/athletic-shoes-534/women/a-t-6356/s/',
        'https://saudi.souq.com/sa-en/casual-shoes/casual---and---dress-shoes-481/women/fashion-sneakers/a-t-6356-6453/s/',
        'https://saudi.souq.com/sa-en/women/casual---and---dress-shoes-481/heels/a-t-6453/s/',
        'https://saudi.souq.com/sa-en/wedges/casual---and---dress-shoes-481/a-t/s/',
        'https://saudi.souq.com/sa-en/women/casual---and---dress-shoes-481/casual-sandals%7Cloafers%7Cloafers---and---moccasian%7Cloafers---and---moccasin/a-t-6453/s/',
        'https://saudi.souq.com/sa-en/women/slippers-485/a-t/s/',
        'https://saudi.souq.com/sa-en/women/casual---and---dress-shoes-481%7Csandals-479/wedges%7Ccasual-sandals/a-t-6453/s/',
        'https://saudi.souq.com/sa-en/boots/boots-469/women/a-t-6356/s/'
    ]

    rules = (
        Rule(
            LinkExtractor(allow=('.*(women|woman).*/(i|u)/')) ,callback="parse_item"),
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
        item_category = []
        self.logger.debug(item['product_name'])
        for kwrd in self.category_list.keys():
            if kwrd == 'casual' and 'shoe' in str(item['product_name']).lower().split():
                for pc in self.category_list[kwrd]:
                    item_category.append(pc)
            elif kwrd != 'casual' and str(kwrd).strip().lower() in str(item['product_name']).lower().split():
                self.logger.debug(kwrd)
                for pc in self.category_list[kwrd]:
                    item_category.append(pc)
        if len(item_category) < 1:
            item_category.append({'pc':'Other','sc':'Other','tc':'Other'})
        item['product_categories'] = item_category
        yield item