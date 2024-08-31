#!/bin/sh

# Criar um ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
. venv/bin/activate

# Instalar as dependências do arquivo requirements.txt
pip install -r requirements.txt

# Iniciar o servidor usando PM2 com o nome "Genshin Builder Crawler API"
pm2 start --name "Genshin Builder Crawler API" -- "uvicorn src.app_module:http_server" --host "0.0.0.0" --port "8000"
