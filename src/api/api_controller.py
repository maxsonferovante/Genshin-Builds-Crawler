from nest.core import Controller, Get, Post
from .api_service import ApiService
from .api_model import Api


@Controller("api")
class ApiController:

    def __init__(self, api_service: ApiService):
        self.api_service = api_service
    
    @Get("/")
    def get_api(self):
        return self.api_service.get_api()
        
    @Post("/")
    def add_api(self, api: Api):
        return self.api_service.add_api(api)

