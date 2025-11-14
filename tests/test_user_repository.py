import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.schemas import UserCreate
from app.repositories.user_repository import user_repository
from app.core.security import verify_password
from app.database import Base

@pytest.fixture
async def async_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_factory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session

    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user(async_session):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="123456"
    )

    db_user = await user_repository.create_user(async_session, user_data)

    assert db_user.id is not None
    assert db_user.username == "testuser"
    assert db_user.email == "test@example.com"
    assert db_user.disabled is False
    assert db_user.hashed_password != user_data.password
    assert verify_password("123456", db_user.hashed_password)

@pytest.mark.asyncio
async def test_get_user_by_username(async_session):
    user_data = UserCreate(
        username="lookup_user",
        email="lookup@example.com",
        password="mypass"
    )

    created = await user_repository.create_user(async_session, user_data)
    found = await user_repository.get_user_by_username(async_session, "lookup_user")

    assert found is not None
    assert found.id == created.id
    assert found.username == "lookup_user"

@pytest.mark.asyncio
async def test_get_user_by_email(async_session):
    user_data = UserCreate(
        username="email_user",
        email="email@example.com",
        password="password"
    )

    created = await user_repository.create_user(async_session, user_data)
    found = await user_repository.get_user_by_email(async_session, "email@example.com")

    assert found is not None
    assert found.id == created.id
    assert found.email == "email@example.com"

@pytest.mark.asyncio
async def test_get_user_by_username_not_found(async_session):
    result = await user_repository.get_user_by_username(async_session, "noexists")
    assert result is None

@pytest.mark.asyncio
async def test_get_user_by_email_not_found(async_session):
    result = await user_repository.get_user_by_email(async_session, "no@mail.com")
    assert result is None
