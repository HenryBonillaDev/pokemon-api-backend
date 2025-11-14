import httpx
from typing import Optional, Dict, Any
from app.core.config import get_settings

settings = get_settings()

class HTTPClient:
    def __init__(self):
        self.base_url = settings.POKEAPI_BASE_URL
        self.timeout = 30.0
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    
    async def get_full_url(self, url: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

http_client = HTTPClient()