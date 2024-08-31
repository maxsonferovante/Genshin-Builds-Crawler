from nest.core import PyNestFactory, Module
from .app_controller import AppController
from .app_service import AppService
from src.crawler.crawler_module import CrawlerModule

@Module(
    imports=[CrawlerModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Este projeto consiste em uma API, desenvolvido em Python, que realiza web crawling para obter informações sobre armas disponíveis para farmar no jogo Genshin Impact",
    title="Genshin Builder Crawler API",
    version="0.0.3",
    debug=True,
    docs_url="/api/docs",
)
http_server = app.get_server()


