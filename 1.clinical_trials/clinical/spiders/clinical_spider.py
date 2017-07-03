#-*- coding: utf-8 -*-
from __future__ import print_function
from clinical.items import ClinicalItem
import scrapy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ClinicalSpider(scrapy.Spider):
	name = "clintrial"
	allowed_domains = ["clinicaltrials.gov"]
	start_urls = ["https://clinicaltrials.gov/ct2/home"]
	
	output_file = open('clinical_trials_result.xls', 'w')
	#输出文件头
	print('Gene', 'Status', 'Title', 'Condition', 'Intervention', 'Phase', 'Nct_url', 'Nct_number', 'Purpose', 'Location', 'Contact', 'Official_title', sep='\t', file=output_file)
	output_file.close()

	def parse(self, response):
		genes_file = './gene.list'
		with open(genes_file) as genes:
			for gene in genes:
				gene = gene.strip()
				yield scrapy.FormRequest.from_response(response, formdata={"term":gene}, meta={'gene':gene}, callback=self.parse_gene)

	def parse_gene(self, response):
		gene = response.meta['gene']
		rank = 2
		all_conditions = response.xpath('//*[contains(text(), "Condition")]/following-sibling::*/text()').extract()
		for each_url in response.xpath('//div[@class="indent1 header3"]/table/tr/td[3]/a/@href').extract():
			if each_url is not None:
				status_xp = '//div[@class="indent1 header3"]/table/tr[{rank}]/td[2]//text()'.format(rank=rank)
				title_xp = '//div[@class="indent1 header3"]/table/tr[{rank}]/td[3]/a/text()'.format(rank=rank)
				condition_xp = '//div[@class="indent1 header3"]/table/tr[{rank}]/td[3]/table/tr[1]/td[@style]/text()'.format(rank=rank)
				intervention_xp = '//div[@class="indent1 header3"]/table/tr[{rank}]/td[3]/table/tr[2]/td/text()'.format(rank=rank)

				status = response.xpath(status_xp).extract()
				title = response.xpath(title_xp).extract()
				condition = all_conditions[rank-2]
				intervention = response.xpath(intervention_xp).extract()

				each_url = response.urljoin(each_url)
				rank += 1

				yield scrapy.Request(each_url, callback=self.parse_nct, meta={'gene':gene, 'status':status, 'title':title, 'condition':condition, 'intervention':intervention})

		next_page = response.xpath('//a[contains(text(),"Next Page")]/@href').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse_gene, meta={'gene':gene})

	def parse_nct(self, response):
		gene = response.meta['gene']
		status = response.meta['status']
		title = response.meta['title']
		condition = response.meta['condition']
		intervention = response.meta['intervention']

		status = "".join(status).replace('\r\n', '').strip().encode("GBK", 'replace').replace("?", " ")
		title = "".join(title).replace('\r\n', '').strip().encode("GBK", 'replace').replace("?", " ")
		condition = "".join(condition).replace('\r\n', ' ').strip().encode("GBK", 'replace').replace("?", " ")
		intervention = "".join(intervention).replace('\r\n', '').strip().encode("GBK", 'replace').replace("?", " ")

		other_infos = ClinicalItem()
		other_infos['url'] = response.url
		other_infos['nct'] = response.xpath('//div[contains(text(), "ClinicalTrials.gov Identifier:")]/following-sibling::*/text()').extract_first()
		#other_infos['purpose'] = "".join(response.xpath('//div[@class="indent1"]/img/following-sibling::*[contains(text(), "Purpose")]/following-sibling::*/div/text()').extract()).replace('\r\n', '').strip().encode("GBK", 'replace').replace("?", " ")
		other_infos['purpose'] = "".join(response.xpath('//div[@class="indent1"]/div[@class="indent2"]/div[@class="body3"]//text()').extract()).replace('\r\n', '').encode("GBK", 'replace').replace("?", " ").replace("\n", "")
		other_infos['phase'] = "".join(response.xpath('//*[@class="indent1"]//table/tr[2]/td[3]//text()').extract()).replace('\r\n', '').encode("GBK", 'replace').replace("?", " ").replace("\n", "")
		pattern = re.compile(r'Phase\s+\d+')
		other_infos['phase'] = "; ".join(pattern.findall(other_infos['phase']))

		#地址和联系方式
		other_infos['location'] = response.xpath('//table[@summary="Layout table for location information"]//text()').extract()
		if other_infos['location']:
			location_list = []
			for i in range(len(other_infos['location'])):
				each_location = other_infos['location'][i].replace("\r\n","").strip()
				if each_location:
					location_list.append(each_location)
			other_infos['location'] = " || ".join(location_list).encode("GBK", 'replace').replace("?", " ").replace("\n", "")

		other_infos['contact'] = response.xpath('//table[@summary="Layout table for location contacts"]//text()').extract()
		if other_infos['contact']:
			contact_list = []
			for i in range(len(other_infos['contact'])):
				each_contact = other_infos['contact'][i].replace("\r\n","").strip()
				if each_contact:
					contact_list.append(each_contact)
			other_infos['contact'] = " || ".join(contact_list).encode("GBK", 'replace').replace("?", " ").replace("\n", "")

		other_infos['official_title'] = "".join(response.xpath('//td[contains(text(), "Official Title")]/following-sibling::*//text()').extract()).replace("\n", "")

		#输出结果
		output_file = open('clinical_trials_result.xls', 'a')
		print(gene, status, title, condition, intervention, other_infos['phase'], other_infos['url'], other_infos['nct'], other_infos['purpose'], other_infos['location'], other_infos['contact'], other_infos['official_title'], sep="\t", file=output_file)
		output_file.close()
