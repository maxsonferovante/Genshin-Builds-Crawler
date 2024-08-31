from .crawler_model import Crawler
from nest.core import Injectable


@Injectable
class CrawlerService:

    def __init__(self):
        self.database = []
        
    def get_crawler(self):
        return self.database
    
    def add_crawler(self, crawler: Crawler):
        self.database.append(crawler)
        return crawler
