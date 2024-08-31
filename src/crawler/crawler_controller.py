from nest.core import Controller, Get, Post
from .crawler_service import CrawlerService
from .crawler_model import Crawler


@Controller("crawler")
class CrawlerController:

    def __init__(self, crawler_service: CrawlerService):
        self.crawler_service = crawler_service
    
    @Get("/")
    def get_crawler(self):
        return self.crawler_service.get_crawler()
        
    @Post("/")
    def add_crawler(self, crawler: Crawler):
        return self.crawler_service.add_crawler(crawler)

