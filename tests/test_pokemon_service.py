import pytest
from unittest.mock import patch, AsyncMock
from app.services.pokemon_service import PokemonService
from app.models.schemas import (
    PokemonDetail,
    PokemonSprites,
    PokemonType,
    PokemonAbility,
    PokemonStat,
    PokemonCompare
)

service = PokemonService()


@pytest.mark.asyncio
@patch("app.utils.http_client.http_client.get", new_callable=AsyncMock)
async def test_get_pokemon_list(mock_get):
    mock_get.return_value = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {"name": "bulbasaur", "url": "url1"},
            {"name": "ivysaur", "url": "url2"},
        ]
    }

    result = await service.get_pokemon_list(limit=2, offset=0)

    assert result.count == 2
    assert len(result.results) == 2
    assert result.results[0].name == "bulbasaur"


@pytest.mark.asyncio
@patch("app.utils.http_client.http_client.get", new_callable=AsyncMock)
async def test_get_pokemon_detail(mock_get):
    mock_get.return_value = {
        "id": 1,
        "name": "bulbasaur",
        "height": 7,
        "weight": 69,
        "base_experience": 64,
        "types": [{"slot": 1, "type": {"name": "grass"}}],
        "abilities": [{"ability": {"name": "overgrow"}, "is_hidden": False}],
        "stats": [{"stat": {"name": "hp"}, "base_stat": 45}],
        "sprites": {
            "front_default": "fd.png",
            "front_shiny": "fs.png",
            "other": {"official-artwork": {"front_default": "art.png"}}
        }
    }

    result = await service.get_pokemon_detail("1")

    assert result.id == 1
    assert result.name == "bulbasaur"
    assert result.sprites.front_default == "fd.png"
    assert result.types[0].name == "grass"
    assert result.stats[0].base_stat == 45


@pytest.mark.asyncio
@patch("app.utils.http_client.http_client.get", new_callable=AsyncMock)
async def test_search_pokemon(mock_get):
    mock_get.return_value = {
        "results": [
            {"name": "pikachu", "url": "url1"},
            {"name": "pidgey", "url": "url2"},
            {"name": "charizard", "url": "url3"}
        ]
    }

    result = await service.search_pokemon("pi")

    assert len(result) == 2
    assert result[0]["name"] == "pikachu"


@pytest.mark.asyncio
@patch("app.services.pokemon_service.PokemonService.get_pokemon_detail")
async def test_compare_pokemon(mock_detail):
    pokemon1 = PokemonDetail(
        id=1,
        name="bulbasaur",
        height=7,
        weight=69,
        base_experience=64,
        types=[PokemonType(name="grass", slot=1)],
        abilities=[PokemonAbility(name="overgrow", is_hidden=False)],
        stats=[PokemonStat(name="hp", base_stat=50)],
        sprites=PokemonSprites(
            front_default="fd.png",
            front_shiny="fs.png",
            official_artwork="art.png"
        )
    )

    pokemon2 = PokemonDetail(
        id=2,
        name="charmander",
        height=6,
        weight=85,
        base_experience=62,
        types=[PokemonType(name="fire", slot=1)],
        abilities=[PokemonAbility(name="blaze", is_hidden=False)],
        stats=[PokemonStat(name="hp", base_stat=40)],
        sprites=PokemonSprites(
            front_default="fd2.png",
            front_shiny="fs2.png",
            official_artwork="art2.png"
        )
    )

    mock_detail.side_effect = [pokemon1, pokemon2]

    result: PokemonCompare = await service.compare_pokemon("1", "2")

    assert result.winner == "bulbasaur"
    assert result.comparison["total_stats"]["bulbasaur"] == 50
    assert result.comparison["total_stats"]["charmander"] == 40
