# Import the libraries
import scrapy
from datetime import date

# Define the spider class
class AutomotiveSpider(scrapy.Spider):
    # Name the spider
    name = "automotive_spider"
    login_url = "https://www.kleverig.eu/login.php?do=login"
    start_urls = ["https://www.kleverig.eu/forumdisplay.php?f=82"]

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        # send a POST request to it
        data = {
            'vb_login_username': 'KrustyK',
            'vb_login_password': 'CvvY5FHr',
        }
        yield scrapy.FormRequest.from_response(response, formdata=data, callback=self.parse)
        
    # Define the parse method
    def parse(self, response):
        # Find the thread elements
        threads = response.xpath("//*[starts-with(@id, 'thread_')]")
        
        # Loop through the threads
        for thread in threads:
            # Extract the thread data
            title = thread.xpath(".//a[@class='title']/text()").get()
            print(f'Thread title: {title}')
            #url = thread.xpath(".//a[@class='title']/@href").get()
            #url = response.urljoin(url)
            #author = thread.xpath(".//td[3]/div/a/text()").get()
            
            # Check if the thread is from today
            today = date.today().strftime("%m-%d-%Y")
            # if today in url:
            #     # Yield the thread data
            #     yield {
            #         "title": title,
            #         "url": url,
            #         "author": author
            #     }
        
        # Find the next page link
        #next_page = response.xpath("//a[@rel='next']/@href")
        
        # Check if there is a next page
        #if next_page:
            # Follow the next page link
        #    next_page = response.urljoin(next_page)
        #    yield scrapy.Request(next_page, callback=self.parse)