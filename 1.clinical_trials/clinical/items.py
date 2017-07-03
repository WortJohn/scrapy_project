# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ClinicalItem(scrapy.Item):
	gene = scrapy.Field()
	status = scrapy.Field()
	title = scrapy.Field()
	condition = scrapy.Field()
	intervention = scrapy.Field()
	url = scrapy.Field()
	nct = scrapy.Field()
	purpose = scrapy.Field()
	phase = scrapy.Field()

	contact = scrapy.Field()
	location = scrapy.Field()
	official_title = scrapy.Field()
