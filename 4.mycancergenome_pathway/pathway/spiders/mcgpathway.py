#-*- coding: utf-8 -*-
from __future__ import print_function
from pathway.items import PathwayItem
import scrapy

import sys, re
reload(sys)
sys.setdefaultencoding('utf-8')

class McgpathwaySpider(scrapy.Spider):
	name = "mcgpathway"
	allowed_domains = ["mycancergenome.org"]
	start_urls = ["https://www.mycancergenome.org/content/molecular-medicine/pathways/"]

	#输出文件头
	with open('mycancergenome_pathway_result.xls', 'w') as files:
		print("Pathyway", "Gene", "Upstream_pathways", "Downstream_pathways", "Diseases", "Target", "Abstract", "Pathyway_url", "Image_description", sep="\t", file=files)

	def parse(self, response):
		for each_url in response.xpath('//*[@id="section-content-container"]/div/ul/li/a/@href').extract():
			yield scrapy.Request(each_url, callback=self.parse_pathway)

	def parse_pathway(self, response):
		item = PathwayItem()
		item['pathway_url'] = response.url
		item['pathway_name'] = "".join(response.xpath('//*[@id="section-content-container"]/div/h1/text()').extract()).strip()
		item['pathway_description'] = "".join(response.xpath('//*[@id="section-content-container"]/div/p[1]//text()').extract()).replace("\r\n","; ").replace("\n", ".")
		item['image_description'] = "".join(response.xpath('//*[@id="section-content-container"]/div/p[3]//text()').extract()).replace("\r\n","; ").replace("\n", ".")
		item['image_urls'] = response.xpath('//*[@id="section-content-container"]/div/p[2]//a/@href').extract()
		
		yield item

		number = response.xpath('//*[@id="section-content-container"]/div/h3/text()').extract()
		for i in range(len(number)):
			index = '//*[@id="section-content-container"]/div/ul[{site}]//text()'.format(site=i+1)
			if re.search(r'Upstream', number[i]):
				item['upstream'] = "".join(response.xpath(index).extract()).replace("\r\n","; ").replace("\n", "")
			elif re.search(r'Downstream', number[i]):
				item['downstream'] = "".join(response.xpath(index).extract()).replace("\r\n","; ").replace("\n", "")
			elif re.search(r'Therapies', number[i]):
				item['therapy'] = "".join(response.xpath(index).extract()).replace("\r\n","; ").replace("\n", "")
			elif re.search(r'Diseases', number[i]):
				item['disease'] = "".join(response.xpath(index).extract()).replace("\r\n","; ").replace("\n", "")
			elif re.search(r'Genes', number[i]):
				item['genes'] = "".join(response.xpath(index).extract()).replace("\r\n",";").replace("\n", "")
				item['genes'] = item['genes'].split(";")

		for term in ['upstream', 'downstream', 'therapy', 'disease', 'genes']:
			if not dict(item).has_key(term):
				item[term] = ""
		
		#输出结果, 根据涉及到的基因输出每一行
		with open('mycancergenome_pathway_result.xls', 'a') as files:
			if item['genes']:							#判断基因list是否存在
				for i, gene in enumerate(item['genes']):
					if gene:							#基因list存在,但生成的基因list元素中存在空的,需要判断
						print(item['pathway_name'], gene, item['upstream'], item['downstream'], item['disease'], item['therapy'], item['pathway_description'], item['pathway_url'], item['image_description'], sep="\t", file=files)
			else:
				print(item['pathway_name'], item['genes'], item['upstream'], item['downstream'], item['disease'], item['therapy'], item['pathway_description'], item['pathway_url'], item['image_description'], sep="\t", file=files)
