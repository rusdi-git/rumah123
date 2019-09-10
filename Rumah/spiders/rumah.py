import scrapy
from ..items import RumahItem

class RumahSpider(scrapy.Spider):
    name = 'rumah'
    start_urls = ['https://www.rumah123.com/jual/bandung/gudang',]
    page = 1

    def get_number(self,text):
        result=''
        try:
            iter(text)
        except TypeError:
            return None
        for i in text:
            try:
                result+=str(int(i))
            except ValueError:
                continue
        if result:
            return int(result)
        else:
            return None

    def parse(self, response):
        list_rumah = response.css('ul.listing-list')
        print(list_rumah)
        for url in list_rumah.css('a::attr(href)'):
            yield response.follow(url, callback=self.parse_detail)
        pages = response.css('li.ant-pagination-item::attr(title)').getall()
        for i in pages:
            try:
                if int(i)==self.page+1:
                    self.page=int(i)
                    yield response.follow(self.start_urls[0]+'/?page={}'.format(self.page), callback=self.parse)
                    break
            except ValueError:
                continue
            
    def parse_detail(self, response):
        item = RumahItem()
        price = response.css('div.property-price').css('span::text').get()
        item['price']=self.get_number(price)
        item['address'] = response.css('span.property-address sale-default::text').get()
        item['supplyImageUrls'] = response.css('header').xpath('..').css('img::attr(src)').get()
        item['luastanah'] = self.get_number(response.css('div.property-areas-info').css('li::text').getall()[1])
        item['luasbangunan'] = self.get_number(response.css('div.property-areas-info').css('li::text').getall()[0])
        item['deskripsi'] = response.css('pre.property-description::text').get().replace('\n',',')
        item['title'] = response.css('h2.description-title::text').get()
        item['url'] = response.url
        yield item