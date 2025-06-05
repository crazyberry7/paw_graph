from typing import Any, Dict, Optional
from api.types.types import Pet, Organization, Contact  # Assuming these are defined in types.py
import httpx, os, time
from dotenv import load_dotenv

load_dotenv()

class PetFinderClient:
    """Client for interacting with the PetFinder API."""
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
    async def get(cls, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = await cls.get_token()
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers={"Authorization": f"Bearer {token}"})
            return res.json()



class PetsResolver:
    """Responsible for transforming raw API data into Pet objects."""

    @classmethod
    async def resolve(cls, location, type, limit) -> list[Pet]:
        res = await cls.fetch_pets(location, type, limit)
        data = res.json()
        pets = []
        for pet in data.get("animals", []):
            pets.append(cls.build_pet(pet))
        return pets

    @classmethod
    async def fetch_pets(cls, location, type, limit) -> Organization:
        url = f"https://api.petfinder.com/v2/animals?location={location}&type={type.capitalize()}&limit={limit}"
        res = await PetFinderClient.get(url)
        return res.json()

    @classmethod
    def build_pet(cls, data: Dict[str, Any]) -> Pet:
        """Build a Pet object from normalized or raw API data."""
        return Pet(
            id=str(data.get("id", "")),
            name=data.get("name", "Unnamed"),
            breed=data.get("breeds", {}).get("primary", "Unknown"),
            age=data.get("age"),
            gender=data.get("gender"),
            description=data.get("description"),
            photo=data.get("photo"),
            contact=cls.parse_contact(data.get("contact")),
        )

    @classmethod
    def parse_contact(cls, data: Optional[Dict[str, Any]]) -> Optional[Contact]:
        if not data:
            return None
        return Contact(
            email=data.get("email"),
            phone=data.get("phone")
        )

