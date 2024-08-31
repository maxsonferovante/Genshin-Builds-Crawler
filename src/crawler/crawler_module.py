from nest.core import Module
from .crawler_controller import CrawlerController
from .crawler_service import CrawlerService


@Module(
    controllers=[CrawlerController],
    providers=[CrawlerService],
    imports=[]
)   
class CrawlerModule:
    pass

    