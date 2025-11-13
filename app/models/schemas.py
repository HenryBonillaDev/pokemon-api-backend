from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    disabled: bool
    
    class Config:
        from_attributes = True

class PokemonBasic(BaseModel):
    name: str
    url: str

class PokemonListResponse(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokemonBasic]

class PokemonAbility(BaseModel):
    name: str
    is_hidden: bool

class PokemonType(BaseModel):
    name: str
    slot: int

class PokemonStat(BaseModel):
    name: str
    base_stat: int

class PokemonSprites(BaseModel):
    front_default: Optional[str]
    front_shiny: Optional[str]
    official_artwork: Optional[str]

class PokemonDetail(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    base_experience: int
    types: List[PokemonType]
    abilities: List[PokemonAbility]
    stats: List[PokemonStat]
    sprites: PokemonSprites

class PokemonCompare(BaseModel):
    pokemon1: PokemonDetail
    pokemon2: PokemonDetail
    winner: Optional[str]
    comparison: dict