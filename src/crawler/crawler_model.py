
from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime

class EnumCrawler(Enum):
    WEAPON = 'weapon'
    CHARACTER = 'character'
    DUNGEON = 'dungeon'

class Item(BaseModel):
    name: Optional[str]
    url: Optional[str]
    img: Optional[str]


class CrawlerResponse(BaseModel):    
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    location: str = Field(init=False,default='Brazil')
    option: Optional[EnumCrawler]
    data: Optional[Dict[str, List[Item]]] = {}
    
class MemberTeam(BaseModel):
    name: str
    position: str
    url: str
    img: str

class TeamsResponse(BaseModel):
    date_formed: datetime = Field(init=False, default_factory=datetime.now)
    bestTeamForCharacter: str
    members: Optional[List[MemberTeam]] = []
