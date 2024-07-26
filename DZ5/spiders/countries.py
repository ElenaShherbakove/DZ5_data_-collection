import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["finance.yahoo.com"]
    start_urls = ["https://finance.yahoo.com/trending-tickers"]

    def parse(self, response):
        countries = response.xpath("//table/tbody/tr")
        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            link = country.xpath(".//@href").get()
            yield(
                #'country_name': name,
                #'link': link
                #scrapy.Request(url=link)
                response.follow(url=link, callback= self.parse_country, meta={'name': name})
            )
    def parse_country(self, response):
        name = response.request.meta['name']
        rows = response.xpath("//*[@id='nimbus-app']/section/section/section/article/section[1]")
        for row in rows:
            #date = row.xpath(".//td/text()").get().strip()
            #open = row.xpath(".//td[2]/text()").get()
            #high = row.xpath(".//td[3]/text()").get()
            #low = row.xpath(".//td[4]/text()").get()
            #close = row.xpath(".//td[5]/text()").get()
            #adj_close = row.xpath(".//td[6]/text()").get()
            #volume = row.xpath(".//td[7]/text()").get()
            name_full = row.xpath(".//h1/text()").get()

            yield{
                'name': name,
                'name_full': name_full
                #'date': date,
                #'open': open,
                #'high': high,
                #'low': low,
                #'close': close,
                #'adj_close': adj_close,
                #'volume': volume
            }

