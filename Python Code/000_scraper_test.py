from scrapy.crawler import CrawlerProcess
from web_scraper import AutomotiveSpider  # assuming the spider is defined in a module named "web_scraper"

process = CrawlerProcess()
process.crawl(AutomotiveSpider)
process.start()