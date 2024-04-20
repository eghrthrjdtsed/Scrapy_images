import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplashItem
from itemloaders.processors import MapCompose


class UnsplashImgSpider(CrawlSpider):
    name = "unsplash_img"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='aD8H3']"), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='oaSYM ZR5jm']"), callback="parse_item", follow=True),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=UnsplashItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        name = response.xpath("(//div[@class='WxXog']/img/@alt)[1]").get()
        loader.add_value('name', name)

        loader.add_xpath('category', "//span[@class='gS_hS ZR5jm']/a/text()")
        img_urls = response.xpath("(//img[contains(@class, 'UD5UQ')]/@src)[1]").get()
        loader.add_value('image_url', img_urls)

        yield loader.load_item()

