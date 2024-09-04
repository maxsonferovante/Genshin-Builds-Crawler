
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

class ItemDungeon(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    
class WeaponsResponse(BaseModel):    
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    location: str = Field(init=False,default='Brazil')
    option: Optional[EnumCrawler]
    data: Optional[Dict[str, List[Item]]] = {}

class CharacterResponse(BaseModel):    
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    location: str = Field(init=False,default='Brazil')
    option: Optional[EnumCrawler]
    data: Optional[Dict[str, List[Item]]] = {}

class DungeonsResponse(BaseModel):    
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    location: str = Field(init=False,default='Brazil')
    option: Optional[EnumCrawler]
    data: Optional[Dict[str, List[ItemDungeon]]] = {}

class MemberTeam(BaseModel):
    name: str
    position: str
    url: str
    img: str

class Team(BaseModel):
    date_formed: datetime = Field(init=False, default_factory=datetime.now)
    bestTeamForCharacter: Optional[str]
    members: Optional[List[MemberTeam]] = []

class TeamsResponse(BaseModel):
    created_at: datetime = Field(init=False, default_factory=datetime.now)
    quantity_teams: Optional[int] = 0
    data: Optional[List[Team]] = []
    
