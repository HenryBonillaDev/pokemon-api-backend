import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.main import app
from app.models.schemas import (
    PokemonDetail, PokemonType, PokemonAbility,
    PokemonStat, PokemonSprites, PokemonListResponse, PokemonCompare
)

client = TestClient(app)

def get_mock_token():
    from app.core.security import create_access_token
    return create_access_token(data={"sub": "testuser"})


@patch('app.services.pokemon_service.pokemon_service.get_pokemon_list')
def test_list_pokemon_requires_auth(mock_list):
    response = client.get("/pokemon/")
    assert response.status_code == 401


@patch('app.services.pokemon_service.pokemon_service.get_pokemon_list')
@patch('app.repositories.user_repository.user_repository.get_user_by_username')
def test_list_pokemon_success(mock_user, mock_list):
    from app.models.user import User
    mock_user.return_value = User(
        id=1, username="testuser",
        email="test@test.com",
        hashed_password="hash",
        disabled=False
    )

    token = get_mock_token()

    mock_list.return_value = PokemonListResponse(
        count=1,
        next=None,
        previous=None,
        results=[{"name": "bulbasaur", "url": "some-url"}]
    )

    response = client.get(
        "/pokemon/?limit=20&offset=0",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["count"] == 1


@patch('app.services.pokemon_service.pokemon_service.search_pokemon')
def test_search_pokemon_requires_auth(mock_search):
    response = client.get("/pokemon/search?name=bulb")
    assert response.status_code == 401


@patch('app.services.pokemon_service.pokemon_service.search_pokemon')
@patch('app.repositories.user_repository.user_repository.get_user_by_username')
def test_search_pokemon_success(mock_user, mock_search):
    from app.models.user import User
    mock_user.return_value = User(
        id=1, username="testuser",
        email="test@test.com",
        hashed_password="hash",
        disabled=False
    )

    token = get_mock_token()

    mock_search.return_value = [
        {"name": "bulbasaur", "url": "some-url"}
    ]

    response = client.get(
        "/pokemon/search?name=bulb",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


@patch('app.services.pokemon_service.pokemon_service.compare_pokemon')
def test_compare_pokemon_requires_auth(mock_compare):
    response = client.get("/pokemon/compare?pokemon1=a&pokemon2=b")
    assert response.status_code == 401


@patch('app.services.pokemon_service.pokemon_service.compare_pokemon')
@patch('app.repositories.user_repository.user_repository.get_user_by_username')
def test_compare_pokemon_success(mock_user, mock_compare):
    from app.models.user import User
    from app.models.schemas import (
        PokemonDetail, PokemonType, PokemonAbility,
        PokemonStat, PokemonSprites, PokemonCompare
    )

    mock_user.return_value = User(
        id=1,
        username="testuser",
        email="test@test.com",
        hashed_password="hash",
        disabled=False
    )

    token = get_mock_token()

    bulbasaur = PokemonDetail(
        id=1,
        name="bulbasaur",
        height=7,
        weight=69,
        base_experience=64,
        types=[PokemonType(name="grass", slot=1)],
        abilities=[PokemonAbility(name="overgrow", is_hidden=False)],
        stats=[PokemonStat(name="hp", base_stat=45)],
        sprites=PokemonSprites(
            front_default="url1",
            front_shiny="url2",
            official_artwork="url3"
        )
    )

    charmander = PokemonDetail(
        id=4,
        name="charmander",
        height=6,
        weight=85,
        base_experience=62,
        types=[PokemonType(name="fire", slot=1)],
        abilities=[PokemonAbility(name="blaze", is_hidden=False)],
        stats=[PokemonStat(name="hp", base_stat=39)],
        sprites=PokemonSprites(
            front_default="urlA",
            front_shiny="urlB",
            official_artwork="urlC"
        )
    )

    mock_compare.return_value = PokemonCompare(
        pokemon1=bulbasaur,
        pokemon2=charmander,
        winner="bulbasaur",
        comparison={"attack": "bulbasaur wins"}
    )

    response = client.get(
        "/pokemon/compare?pokemon1=bulbasaur&pokemon2=charmander",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


@patch('app.services.pokemon_service.pokemon_service.get_pokemon_detail')
@patch('app.repositories.user_repository.user_repository.get_user_by_username')
def test_get_pokemon_detail_success(mock_user, mock_detail):
    from app.models.user import User
    mock_user.return_value = User(
        id=1, username="testuser",
        email="test@test.com",
        hashed_password="hash",
        disabled=False
    )

    token = get_mock_token()

    mock_detail.return_value = PokemonDetail(
        id=1,
        name="bulbasaur",
        height=7,
        weight=69,
        base_experience=64,
        types=[PokemonType(name="grass", slot=1)],
        abilities=[PokemonAbility(name="overgrow", is_hidden=False)],
        stats=[PokemonStat(name="hp", base_stat=45)],
        sprites=PokemonSprites(
            front_default="url",
            front_shiny="url",
            official_artwork="url"
        )
    )

    response = client.get(
        "/pokemon/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "bulbasaur"
