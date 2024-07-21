import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["finance.yahoo.com"]
    start_urls = ["https://finance.yahoo.com/trending-tickers/?guccounter=1&guce_referrer=aHR0cHM6Ly9lZHUubGl2ZWRpZ2l0YWwuc3BhY2Uv&guce_referrer_sig=AQAAADGHJGtm3-4AUeC5nljuKtS_fiU1h8Qp4xlyIwrpiyYKPxo59E-QsLol8eJ5Mws0P0mUew9a19MP_dXQTFJVPLDag86uVKwQ5iWUyOSFdinelpbQ_QfSFm5YHaSH6aNhcbprdYXBw2GaKrxdYTFQFm7HivjPfyjOHUUNJR6J2YOb/"]

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            yield{
                #'country_name': name,
                #'link': link
                #scrapy.Request(url=link)
                response.follow(url=link, callback= self.parse_country, meta={'country_name': name})
            }
    def parse_country(self, response):
        rows = response.xpath("//tr[contains(@class, 'yf-ewueuo')]")
        for row in rows:
            date = row.xpath(".//td/text()").get()
            open = float(row.xpath(".//td[2]/text()").get())
            high = float(row.xpath(".//td[3]/text()").get())
            low = float(row.xpath(".//td[4]/text()").get())
            close = float(row.xpath(".//td[5]/text()").get())
            adj_close = float(row.xpath(".//td[6]/text()").get())
            volume = float(row.xpath(".//td[7]/text()").get())
            name = response.request.meta['country_name']

            yield{
                'country_name': name,
                'date': date,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'adj_close': adj_close,
                'volume': volume
            }

