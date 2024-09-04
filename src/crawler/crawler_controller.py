from nest.core import Controller, Get, Post
from .crawler_service import CrawlerService
from .crawler_model import EnumCrawler, WeaponsResponse, CharacterResponse, DungeonsResponse, TeamsResponse


@Controller("crawler")
class CrawlerController:

    def __init__(self, crawler_service: CrawlerService):
        self.crawler_service = crawler_service
    
    @Get("/weapons")
    def get_crawler_weapons(self) -> WeaponsResponse:
        return self.crawler_service.get_weapon(EnumCrawler.WEAPON)
    
    @Get("/characters")
    def get_crawler_characters(self) -> CharacterResponse:
        return self.crawler_service.get_character(EnumCrawler.CHARACTER)
        
    @Get("/dungeons")
    def get_crawler_dungeons(self) -> DungeonsResponse:
        return self.crawler_service.get_dungeon()
    
    @Get("/teams")
    def get_crawler_teams(self) -> TeamsResponse:
        return self.crawler_service.get_teams()