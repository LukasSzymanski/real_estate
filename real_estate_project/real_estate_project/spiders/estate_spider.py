import scrapy
from scrapy.crawler import CrawlerProcess
from items import RealEstateItem


class SelectEstate(scrapy.Spider):
    name = 'komornik'
    search_url = 'https://licytacje.komornik.pl/Notice/Search'
    start_urls = [search_url]

    def __init__(self, jid):
        scrapy.Spider.__init__(self)
        self.jid = jid

    def parse(self, response):
        self.logger.info(f'{self.name} start parse')
        token = response.css('input[name="__RequestVerificationToken"]::attr(value)').extract_first()
        data = {
            "__RequestVerificationToken": token,
            "Type": '1',
            "JudgmentId": self.jid
        }
        self.logger.info(f'{self.name} yield {data}')
        yield scrapy.FormRequest(url=self.search_url, formdata=data, callback=self.parse_adverts)

    def parse_adverts(self, response):
        self.logger.info(f'{self.name} start parse_adverts')
        items = RealEstateItem()
        self.logger.info(f'{self.name} start quotes')
        table = response.css('table.wMax')
        rows = table.css('tr')
        for row in rows[1:]:
            items = row.css('td')
            data = {
                'date': items[2].css('td::text').get().strip(),
                'category': items[3].css('td::text').get().strip(),
                'description': items[4].css('div::text').get().strip(),
                'city': items[5].css('td::text').get().strip(),
                'price': items[6].css('td::text').get().strip(),
                'url': items[8].css('a::attr(href)').get(),
            }
            yield data


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })

    process.crawl(SelectEstate, jid='1068')
    process.start()
