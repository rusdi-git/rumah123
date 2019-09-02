import scrapy
from ..items import RumahItem

class RumahSpider(scrapy.Spider):
    name = 'rumah'
    start_urls = ['https://www.rumah123.com/jual/bandung/gudang',]

    def get_text(self,text):
        result=''
        for i in text:
            try:
                result+=str(int(i))
            except ValueError:
                continue
        return int(result)

    def parse(self, response):
        list_rumah = response.css('ul.listing-list')
        list_url = list_rumah.css('a::attr(href)')
        for url in list_url:
            yield response.follow(url, callback=self.parse_detail)

    def parse_detail(self, response):
        item = RumahItem()
        price_div = response.css('div.property-price')
        price = price_div.css('span::text').get()
        item['price']=self.get_text(price)
        item['address'] = response.css('span.property-address sale-default::text').get()
        # item['supplyImageUrls'] = back_button.xpath('..').css('img::attr(src)').get()
        item['luastanah'] = response.css('div.property-areas-info').css('li::text').getall()[1]
        item['luasbangunan'] = response.css('div.property-areas-info').css('li::text').getall()[0]
        item['deskripsi'] = response.css('pre.property-description::text').get()
        yield item
