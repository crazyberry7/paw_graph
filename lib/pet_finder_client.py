import os, time, httpx
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv() # loads environment variables from a .env file

class PetFinderClient:
    """Client for interacting with the PetFinder API."""
    BASE_URL = "https://api.petfinder.com/v2"
    # url = f"https://api.petfinder.com/v2/animals?location={location}&type={type.capitalize()}&limit={limit}"
    PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
    PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")
    _token_cache = {"token": None, "expires_at": 0}

    @classmethod
    async def get_token(cls):
        now = time.time()
        if cls._token_cache["token"] and now < cls._token_cache["expires_at"]:
            return cls._token_cache["token"]

        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://api.petfinder.com/v2/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": cls.PETFINDER_CLIENT_ID,
                    "client_secret": cls.PETFINDER_CLIENT_SECRET
                }
            )
            data = res.json()
            cls._token_cache["token"] = data["access_token"]
            cls._token_cache["expires_at"] = now + data["expires_in"] - 10
            return cls._token_cache["token"]

    @classmethod
    async def get_adoptable_pets(cls, params: Optional[Dict[str, Any]] = None) -> list[Dict[str, Any]]:
        token = await cls.get_token()
        url = f"https://api.petfinder.com/v2/animals?location={params.get("location")}&type={params.get("type")}&limit={params.get("limit")}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers={"Authorization": f"Bearer {token}"},
                                        params=params)
        return res.json().get("animals", [])

    @classmethod
    async def get(cls, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = await cls.get_token()
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers={"Authorization": f"Bearer {token}"}, params=params)
            res.raise_for_status()
            return res.json()
