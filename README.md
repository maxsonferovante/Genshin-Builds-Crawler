# Genshin Builder Crawler API

Este projeto consiste em uma API, desenvolvido em Python, que realiza web crawling para obter informações sobre armas disponíveis para farmar no jogo Genshin Impact.

## Start Service

## Step 1 - Create environment

- install requirements:

```bash
pip install -r requirements.txt
```

## Step 2 - start service local

1. Run service with main method

```bash
python main.py
```

2. Run service using uvicorn

```bash
uvicorn "app:app" --host "0.0.0.0" --port "8000" --reload
```

## Step 3 - Send requests

Go to the fastapi docs and use your api endpoints - http://127.0.0.1/api/docs
