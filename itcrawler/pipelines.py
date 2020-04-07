# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import random

class ItcrawlerPipeline(object):
	def create_hash(self,*args):
			m = hashlib.md5()
			for arg in args:
				m.update(str(arg).replace("\n","").encode('utf-8')) 

			data = m.hexdigest()
			return data;


	def process_item(self, item, spider):
		args = item['title'] + item['price range'] + item['company'] + item['city']
		for k in item['keywords']:
			args = args + k
		item['hash_id'] = self.create_hash(args)
		return item
