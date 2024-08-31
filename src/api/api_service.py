from .api_model import Api
from nest.core import Injectable


@Injectable
class ApiService:

    def __init__(self):
        self.database = []
        
    def get_api(self):
        return self.database
    
    def add_api(self, api: Api):
        self.database.append(api)
        return api
