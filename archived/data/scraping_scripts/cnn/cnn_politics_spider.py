# Run: scrapy runspider cnn_politics_spider.py -o ../../raw/cnn/urls.json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


def set_priority(request, spider):
    """
    Process each request and assign a priority based on the year found in the URL.
    Newer articles (with higher year values) receive a higher priority.
    """
    match = re.search(r"/(\d{4})/", request.url)
    if match:
        year = int(match.group(1))
        # Subtract a baseline (e.g., 2000) to keep numbers reasonable.
        # Newer articles get a higher priority.
        request.priority = year - 2000
    return request


class CnnPoliticsSpider(CrawlSpider):
    name = "cnn_politics"
    allowed_domains = ["cnn.com"]
    start_urls = ["https://www.cnn.com/politics"]

    # Allow handling of HTTP 451 responses (legal/regional blocks)
    handle_httpstatus_list = [451]

    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/109.0.0.0 Safari/537.36"
        ),
        "HTTPERROR_ALLOWED_CODES": [451],
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    rules = (
        # Rule to follow URLs that look like CNN articles (with date + "politics" in the URL)
        Rule(
            LinkExtractor(allow=(r"/\d{4}/\d{2}/\d{2}/politics/",)),
            callback="parse_item",
            follow=True,
            process_request=set_priority,  # Adjust request priority based on year.
        ),
        # Follow any URL containing '/politics' to traverse section pages.
        Rule(LinkExtractor(allow=(r"/politics",)), follow=True),
    )

    def parse_item(self, response):
        if response.status == 451:
            self.logger.warning(f"Received HTTP 451 for URL: {response.url}")

        title = response.css("h1::text").get()

        # Attempt several common selectors to extract the body paragraphs.
        body_paragraphs = response.css("div.zn-body__paragraph::text").getall()
        if not body_paragraphs:
            body_paragraphs = response.css("div.l-container p::text").getall()
        if not body_paragraphs:
            body_paragraphs = response.css("article p::text").getall()
        if not body_paragraphs:
            body_paragraphs = response.css("div.Article__content p::text").getall()

        body = "\n".join(body_paragraphs).strip()

        if not body:
            self.logger.warning(f"No body content found for {response.url}")

        yield {
            "url": response.url,
            "status": response.status,
            "title": title,
            "body": body,
        }
