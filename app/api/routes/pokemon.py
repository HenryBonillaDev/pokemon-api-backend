from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from app.models.schemas import (
    PokemonListResponse, 
    PokemonDetail, 
    PokemonCompare,
    TokenData
)
from app.services.pokemon_service import pokemon_service
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/pokemon", tags=["Pokemon"])

@router.get("/", response_model=PokemonListResponse)
async def list_pokemon(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: TokenData = Depends(get_current_user)
):
    try:
        return await pokemon_service.get_pokemon_list(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[Dict[str, str]])
async def search_pokemon(
    name: str = Query(..., min_length=1),
    current_user: TokenData = Depends(get_current_user)
):
    try:
        return await pokemon_service.search_pokemon(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare", response_model=PokemonCompare)
async def compare_pokemon(
    pokemon1: str = Query(...),
    pokemon2: str = Query(...),
    current_user: TokenData = Depends(get_current_user)
):
    try:
        return await pokemon_service.compare_pokemon(pokemon1, pokemon2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{pokemon_id}", response_model=PokemonDetail)
async def get_pokemon(
    pokemon_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    try:
        return await pokemon_service.get_pokemon_detail(pokemon_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Pokemon not found: {str(e)}")