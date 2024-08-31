from nest.core import Module
from .api_controller import ApiController
from .api_service import ApiService


@Module(
    controllers=[ApiController],
    providers=[ApiService],
    imports=[]
)   
class ApiModule:
    pass

    