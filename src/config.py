from dotenv import load_dotenv
import os
load_dotenv()

configs = {
    'url_base': os.getenv('URL_BASE'),
    'port': int(os.getenv('PORT') or "8000"),
}