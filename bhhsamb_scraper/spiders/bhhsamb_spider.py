import scrapy
from bhhsamb_scraper.items import PropertyItem

class BhhsambSpider(scrapy.Spider):
    name = 'bhhsamb'
    allowed_domains = ['bhhsamb.com']
    start_urls = ['https://www.bhhsamb.com/agents']

    def parse(self, response):
        self.logger.info("Parsing the main page: %s", response.url)
        
        # Extract links to individual property/person pages
        profile_links = response.xpath('//div[@class="cms-int-roster-card-content site-roster-card-content"]/ul/li/a/@href').extract()
        self.logger.info("Found %d profile links", len(profile_links))
        
        for link in profile_links:
            yield response.follow(link, self.parse_property)

        # Follow pagination links if available (adjust if pagination exists)
        next_page = response.xpath('//a[@title="Next"]/@href').extract_first()
        if next_page:
            self.logger.info("Following pagination link: %s", next_page)
            yield response.follow(next_page, self.parse)
        else:
            self.logger.info("No more pagination links found.")

    def parse_property(self, response):
        self.logger.info("Parsing property/person page: %s", response.url)
        
        item = PropertyItem()
        item['name'] = response.xpath('//div[@class="cms-int-roster-card-content site-roster-card-content"]/h2/text()').extract_first()
        item['title'] = response.xpath('//div[@class="site-roster-card-content-title"]/span/text()').extract_first()
        item['phone'] = response.xpath('//ul/li/a[contains(@href, "tel:")]/text()').extract_first()
        item['email_link'] = response.xpath('//ul/li/a[contains(@href, "Contact")]/@href').extract_first()
        item['profile_link'] = response.xpath('//ul/li/a[contains(@href, "bhhsamb.com")]/@href').extract_first()
        item['office'] = response.xpath('//ul/li[last()]/text()').extract_first()
        item['url'] = response.url

        # Print extracted data to console
        print("Name:", item['name'])
        print("Title:", item['title'])
        print("Phone:", item['phone'])
        print("Email Link:", item['email_link'])
        print("Profile Link:", item['profile_link'])
        print("Office:", item['office'])
        print("URL:", item['url'])
        print("-------------")

        yield item
