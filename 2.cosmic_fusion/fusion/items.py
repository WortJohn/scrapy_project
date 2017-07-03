# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FusionItem(scrapy.Item):
	#10列的信息表格
	all_fusion_urls = scrapy.Field()			#所有融合的URL
	fusion_id = scrapy.Field()					#融合基因id, 如:COSF688
	fusion_gene = scrapy.Field()				#两个融合基因的名字
	fusion_url = scrapy.Field()					#fusion_id对应的URL 如:http://cancer.sanger.ac.uk/cosmic/fusion/summary?id=999
	gene1 = scrapy.Field()						#基因1
	exon1 = scrapy.Field()						#外显子1
	breakpoint1 = scrapy.Field()				#断点1
	gene2 = scrapy.Field()						#基因2
	exon2 = scrapy.Field()						#外显子2
	breakpoint2 = scrapy.Field()				#断点2
	mutation_number = scrapy.Field()			#突变数目
	mutation_frequency = scrapy.Field()			#突变频率
