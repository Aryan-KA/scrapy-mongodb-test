import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"    # unique spider name
    start_urls = [
        "https://quotes.toscrape.com"
    ]

    def parse(self, response):
        # loop over every quote block on the page
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("a.tag::text").getall()
            }

        # Follow the "next" button - this is what makes it a crawler
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)