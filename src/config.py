from dotenv import load_dotenv
import os
load_dotenv()

configs = {
    'url_base': os.getenv('URL_BASE'),
}