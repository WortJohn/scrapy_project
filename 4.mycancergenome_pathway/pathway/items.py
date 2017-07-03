# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PathwayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	image_urls = scrapy.Field()
	image_paths = scrapy.Field()

	pathway_url = scrapy.Field()		#每个pathway的url
	pathway_name = scrapy.Field()		#每个pathway的名称
	pathway_description = scrapy.Field()		#每个pathway的描述
	image_description = scrapy.Field()		#每个pathway图片的描述
	upstream = scrapy.Field()
	downstream = scrapy.Field()
	disease = scrapy.Field()
	therapy = scrapy.Field()
	genes = scrapy.Field()
