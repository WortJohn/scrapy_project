# -*- coding: utf-8 -*-
from __future__ import print_function
from fusion.items import FusionItem
import scrapy
from scrapy.http import Request

class FusionSpider(scrapy.Spider):
	name = "fusion"
	allowed_domains = ["sanger.ac.uk"]
	start_urls = ["http://grch37-cancer.sanger.ac.uk/cosmic/fusion"]
	#输出表头
	output_file = open('cosmic_fusion.xls', 'w')
	print('Fusion_genes', 'Fusion_id', 'Fusion_url', 'Gene1', 'Exon1', 'Breakpoint1', 'Gene2', 'Exon2', 'Breakpoint2', 'Mutation_number','Mutation_frequency', sep='\t', file=output_file)
	output_file.close()
	def parse(self, response):
		a = response.body
		print("测试", a)
		

	#def start_requests(self):
	#	all_urls = []
		#with open('all_url.xls') as file:
		#	for f in file:
		#		all_urls.append(f.strip())
		#start_urls = all_urls
		#for each_url in start_urls:
		#	yield Request(url=each_url, callback=self.parse)
		#start_url = "http://grch37-cancer.sanger.ac.uk/cosmic/fusion"
		

#	def parse(self, response):
#		fusion_gene_item = FusionItem()
#		fusion_id_item = FusionItem()
#		fusion_url_item = FusionItem()
#		gene1_item = FusionItem()
#		exon1_item = FusionItem()
#		breakpoint1_item = FusionItem()
#		gene2_item = FusionItem()
#		exon2_item = FusionItem()
#		breakpoint2_item = FusionItem()
#		mutation_number_item = FusionItem()
#		mutation_frequency_item = FusionItem()
#
#		fusion_gene_item['fusion_gene'] = "".join(response.xpath('//*[@id="overview"]/div[2]/div[2]//text()').extract())
#		fusion_id_item['fusion_id']	= response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[1]/a/text()').extract()
#		fusion_url_item['fusion_url'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[1]/a/@href').extract()
#		gene1_item['gene1'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[2]/a/text()').extract()
#		exon1_item['exon1'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[3]/text()').extract()
#		breakpoint1_item['breakpoint1'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[4]/text()').extract()
#		gene2_item['gene2'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[6]/a/text()').extract()
#		exon2_item['exon2'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[7]/text()').extract()
#		breakpoint2_item['breakpoint2'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[8]/text()').extract()
#		mutation_number_item['mutation_number'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[10]/text()').extract()
#		mutation_frequency_item['mutation_frequency'] = response.xpath('//*[@id="overview"]/div[2]/div[3]/table//tr/td[11]/text()').extract()
#		#输出内容
#		output_file = open('cosmic_fusion.xls', 'a')
#		for i in range(len(fusion_id_item['fusion_id'])):
#			contents = "{genes}\t{id}\t{url}\t{gene1}\t{exon1}\t{breakpoint1}\t{gene2}\t{exon2}\t{breakpoint2}\t{number}\t{frequency}".format(genes=fusion_gene_item['fusion_gene'], id=fusion_id_item['fusion_id'][i], url=fusion_url_item['fusion_url'][i], gene1=gene1_item['gene1'][i], exon1=exon1_item['exon1'][i], breakpoint1=breakpoint1_item['breakpoint1'][i], gene2=gene2_item['gene2'][i], exon2=exon2_item['exon2'][i], breakpoint2=breakpoint2_item['breakpoint2'][i], number=mutation_number_item['mutation_number'][i], frequency=mutation_frequency_item['mutation_frequency'][i])
#			print(contents, file=output_file)
#		output_file.close()
