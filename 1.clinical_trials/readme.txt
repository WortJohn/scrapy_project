1. 起始url
https://clinicaltrials.gov/ct2/home

2. 输入---------注意修改gene list路径---------
基因list文件,每行一个gene name; 运行之前需要修改clinical/spiders/clinical_spider.py的genes_file = './gene.list'

3. 输出,如:
./clinical_trials_result.xls

4. 运行命令
nohup scrapy crawl clintrial &
