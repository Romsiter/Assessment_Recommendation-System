import scrapy

class SHLCatalogSpider(scrapy.Spider):
    name = "shl_catalog"
    start_urls = ["https://www.shl.com/solutions/products/product-catalog/"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CLOSESPIDER_ITEMCOUNT': 500,
        'FEED_URI': 'shl_assessments.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        links = response.css('a.custom__table-heading__title-link::attr(href)').getall()
        links += response.css('td.custom__table-heading__title a::attr(href)').getall()

        for href in set(links):
            yield response.follow(href, callback=self.parse_detail)

        next_page = response.css('li.-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for page in response.css('ul.pagination li a::attr(href)').getall():
            yield response.follow(page, callback=self.parse)

    def parse_detail(self, response):
        yield {
            'title': response.css('div.content__container h1::text').get(default='').strip(),
            'url': response.url,
            'description': response.xpath('//div[h4[text()="Description"]]/p/text()').get(default='No description available').strip(),
            'job_levels': response.xpath('//div[h4[text()="Job levels"]]/p/text()').get(default='Not available').strip(),
            'languages': response.xpath('//div[h4[text()="Languages"]]/p/text()').get(default='Not available').strip(),
            'duration_minutes': response.xpath('//div[h4[text()="Assessment length"]]/p/text()').get(default='').strip(),
            'test_types': response.xpath(
                '//p[contains(@class, "product-catalogue__small-text")][contains(., "Test Type")]/span//span[@class="product-catalogue__key"]/text()'
            ).getall(),
            'remote_testing': 'Yes' if response.xpath('//p[contains(., "Remote Testing")]/span[contains(@class, "-yes")]') else 'No',
            'adaptive_supported': (
                response.xpath('//li[contains(., "Adaptive") or contains(., "IRT")]/text()').get(default='No Information').split(':')[-1].strip()
            )
        }
