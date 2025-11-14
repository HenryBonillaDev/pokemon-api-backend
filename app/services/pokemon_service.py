from typing import Dict, Any, List, Optional
from app.utils.http_client import http_client
from app.models.schemas import (
    PokemonListResponse,
    PokemonDetail,
    PokemonType,
    PokemonAbility,
    PokemonStat,
    PokemonSprites,
    PokemonCompare
)

class PokemonService:
    
    async def get_pokemon_list(self, limit: int = 20, offset: int = 0) -> PokemonListResponse:
        try:
            data = await http_client.get("pokemon", params={"limit": limit, "offset": offset})
            return PokemonListResponse(**data)
        except Exception as e:
            raise Exception(f"Error fetching pokemon list: {str(e)}")
    
    async def get_pokemon_detail(self, pokemon_id: str) -> PokemonDetail:
        try:
            data = await http_client.get(f"pokemon/{pokemon_id}")
            
            types = [PokemonType(name=t["type"]["name"], slot=t["slot"]) for t in data["types"]]
            
            abilities = [
                PokemonAbility(name=a["ability"]["name"], is_hidden=a["is_hidden"]) 
                for a in data["abilities"]
            ]
            
            stats = [
                PokemonStat(name=s["stat"]["name"], base_stat=s["base_stat"]) 
                for s in data["stats"]
            ]
            
            sprites = PokemonSprites(
                front_default=data["sprites"].get("front_default"),
                front_shiny=data["sprites"].get("front_shiny"),
                official_artwork=data["sprites"].get("other", {}).get("official-artwork", {}).get("front_default")
            )
            
            return PokemonDetail(
                id=data["id"],
                name=data["name"],
                height=data["height"],
                weight=data["weight"],
                base_experience=data["base_experience"],
                types=types,
                abilities=abilities,
                stats=stats,
                sprites=sprites
            )
        except Exception as e:
            raise Exception(f"Error fetching pokemon detail: {str(e)}")
    
    async def search_pokemon(self, name: str) -> List[Dict[str, str]]:
        try:
            data = await http_client.get("pokemon", params={"limit": 1000, "offset": 0})
            results = [p for p in data["results"] if name.lower() in p["name"].lower()]
            return results[:10]
        except Exception as e:
            raise Exception(f"Error searching pokemon: {str(e)}")
    
    async def compare_pokemon(self, pokemon1_id: str, pokemon2_id: str) -> PokemonCompare:
        try:
            pokemon1 = await self.get_pokemon_detail(pokemon1_id)
            pokemon2 = await self.get_pokemon_detail(pokemon2_id)
            
            total_stats_1 = sum(stat.base_stat for stat in pokemon1.stats)
            total_stats_2 = sum(stat.base_stat for stat in pokemon2.stats)
            
            winner = pokemon1.name if total_stats_1 > total_stats_2 else pokemon2.name
            if total_stats_1 == total_stats_2:
                winner = "tie"
            
            comparison = {
                "total_stats": {
                    pokemon1.name: total_stats_1,
                    pokemon2.name: total_stats_2
                },
                "winner": winner
            }
            
            return PokemonCompare(
                pokemon1=pokemon1,
                pokemon2=pokemon2,
                winner=winner,
                comparison=comparison
            )
        except Exception as e:
            raise Exception(f"Error comparing pokemon: {str(e)}")

pokemon_service = PokemonService()