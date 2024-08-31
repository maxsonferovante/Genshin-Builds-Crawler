import uvicorn
from src.config import configs

if __name__ == '__main__':
    uvicorn.run(
        'src.app_module:http_server',        
        port=configs['port'],
        reload=True
    )
    
