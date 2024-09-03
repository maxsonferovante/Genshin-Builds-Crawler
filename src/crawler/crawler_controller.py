from nest.core import Controller, Get, Post
from .crawler_service import CrawlerService
from .crawler_model import EnumCrawler


@Controller("crawler")
class CrawlerController:

    def __init__(self, crawler_service: CrawlerService):
        self.crawler_service = crawler_service
    
    @Get("/weapons")
    def get_crawler_weapons(self):
        return self.crawler_service.get_weapon(EnumCrawler.WEAPON)
    
    @Get("/characters")
    def get_crawler_characters(self):
        return self.crawler_service.get_character(EnumCrawler.CHARACTER)
        
    

