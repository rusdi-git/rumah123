# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

class RumahPipeline(object):
    init = []
    def process_item(self, item, spider):
        if spider.name == 'rumah':
            with open('result.json','r+') as f:
                data = {k:v for k,v in item.items() if v}
                try:
                    init = json.load(f)
                    init.append(data)
                except json.JSONDecodeError:
                    json.dump([data,],f)
                    init.append(data)
                    return
                
            with open('result.json','w') as file:
                json.dump(init,file)
