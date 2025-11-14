
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, pokemon
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Pokemon API",
    description="API REST that consumes PokeAPI and exposes processed endpoints",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(pokemon.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Pokemon API",
        "docs": "/docs",
        "health": "OK"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}