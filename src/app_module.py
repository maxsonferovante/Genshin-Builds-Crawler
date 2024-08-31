from nest.core import PyNestFactory, Module
from .app_controller import AppController
from .app_service import AppService
from src.crawler.crawler_module import CrawlerModule
from src.api.api_module import ApiModule


@Module(
    imports=[CrawlerModule, ApiModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
)
http_server = app.get_server()
