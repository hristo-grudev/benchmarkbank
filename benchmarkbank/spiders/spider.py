import scrapy

from scrapy.loader import ItemLoader

from ..items import BenchmarkbankItem
from itemloaders.processors import TakeFirst


class BenchmarkbankSpider(scrapy.Spider):
	name = 'benchmarkbank'
	start_urls = ['https://www.benchmarkbank.com/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="read"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="blog_title"]/text()').get()
		description = response.xpath('//div[@class="block-richtext"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=BenchmarkbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
