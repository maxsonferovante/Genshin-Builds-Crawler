from pydantic import BaseModel


class Crawler(BaseModel):
    name: str

