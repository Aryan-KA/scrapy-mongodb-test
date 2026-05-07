# quotesbot/spiders/hn_spider.py
import scrapy
from datetime import datetime

class HackerNewsSpider(scrapy.Spider):
    name = "hackernews"
    start_urls = ["https://news.ycombinator.com/news"]

    def parse(self, response):
        # Each story row has class "athing"
        for row in response.css("tr.athing"):
            story_id = row.attrib.get("id")
            title_el = row.css("span.titleline > a")
            title = title_el.css("::text").get()
            url = title_el.attrib.get("href")

            # The score/date row is the next sibling
            subrow = row.xpath("following-sibling::tr[1]")
            score_text = subrow.css("span.score::text").get(default="0")
            age = subrow.css("span.age::attr(title)").get()  # gives ISO date
            try:
                score = int(score_text.replace(" points", "").strip())
            except (ValueError, AttributeError):
                score = 0

            if title:
                yield {
                    "title": title,
                    "url": url,
                    "score": score,
                    "date": age,          # e.g. "2026-04-27T10:30:00"
                    "source": "Hacker News",
                    "scraped_at": datetime.utcnow().isoformat(),
                }

        # Follow "More" link to next page
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)