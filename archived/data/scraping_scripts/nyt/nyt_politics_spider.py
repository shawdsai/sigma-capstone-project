# Run: scrapy runspider nyt_politics_spider.py -o ../../raw/nyt/urls.json
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def set_priority(request, spider):
    """
    Process each request and assign a priority based on the year found in the URL.
    Newer articles (with higher year values) receive a higher priority.
    """
    match = re.search(r"/(\d{4})/", request.url)
    if match:
        year = int(match.group(1))
        # Subtract a baseline (e.g., 2000) to keep numbers reasonable.
        request.priority = year - 2000
    return request


class NytPoliticsSpider(CrawlSpider):
    name = "nyt_politics"
    allowed_domains = ["nytimes.com"]
    start_urls = ["https://www.nytimes.com/international/section/politics"]

    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/109.0.0.0 Safari/537.36"
        ),
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    rules = (
        # Rule to follow URLs that look like NYT articles
        # e.g. https://www.nytimes.com/2025/02/16/us/politics/trump-europe-alliance-crisis.html
        Rule(
            LinkExtractor(allow=(r"/\d{4}/\d{2}/\d{2}/us/politics/",)),
            callback="parse_item",
            follow=True,
            process_request=set_priority,  # Adjust request priority based on year.
        ),
        # Follow any URL containing '/politics' to help traverse the section.
        Rule(
            LinkExtractor(allow=(r"/politics",)),
            follow=True,
        ),
    )

    def parse_item(self, response):
        title = response.css("h1::text").get()

        # Try to extract the article body using several selectors.
        # NYT articles commonly use a section named "articleBody".
        body_paragraphs = response.css("section[name='articleBody'] p::text").getall()
        if not body_paragraphs:
            # Fallback: try extracting paragraphs from the article element.
            body_paragraphs = response.css("article p::text").getall()
        if not body_paragraphs:
            # Older NYT pages might use this selector.
            body_paragraphs = response.css("p.story-body-text::text").getall()

        body = "\n".join(body_paragraphs).strip()

        if not body:
            self.logger.warning(f"No body content found for {response.url}")

        yield {
            "url": response.url,
            "status": response.status,
            "title": title,
            "body": body,
        }
