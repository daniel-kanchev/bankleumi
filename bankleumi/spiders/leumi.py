import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bankleumi.items import Article


class LeumiSpider(scrapy.Spider):
    name = 'leumi'
    start_urls = ['https://www.bankleumi.co.uk/news']

    def parse(self, response):
        links = response.xpath('//h3[@class="news-article-title"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = " ".join(response.xpath('//p[@class="article-posted-date"]/text()').get().split()[1:-1])
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="col-lg-8 offset-lg-2 article-main"]/div[last()]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        category = response.xpath('//div[@class="article-title-container"]//a/text()').get().strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('category', category)

        return item.load_item()
