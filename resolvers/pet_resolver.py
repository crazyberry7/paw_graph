from typing import Any, Dict, Optional
from api.types.types import Pet, Organization, Contact  # Assuming these are defined in types.py
import httpx, os, time
from dotenv import load_dotenv

load_dotenv()

PETFINDER_CLIENT_ID = os.getenv("PETFINDER_CLIENT_ID")
PETFINDER_CLIENT_SECRET = os.getenv("PETFINDER_CLIENT_SECRET")

_token_cache = {"token": None, "expires_at": 0}

async def get_petfinder_token():
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.petfinder.com/v2/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": PETFINDER_CLIENT_ID,
                "client_secret": PETFINDER_CLIENT_SECRET
            }
        )
        data = res.json()
        _token_cache["token"] = data["access_token"]
        _token_cache["expires_at"] = now + data["expires_in"] - 10
        return _token_cache["token"]

class PetResolver:
    """Responsible for transforming raw API data into Pet objects."""

    @classmethod
    async def fetch_pets(cls, location, type, limit) -> list[Pet]:
        token = await get_petfinder_token()
        url = f"https://api.petfinder.com/v2/animals?location={location}&type={type.capitalize()}&limit={limit}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, headers={"Authorization": f"Bearer {token}"})
            data = res.json()

        pets = []
        for pet in data.get("animals", []):
            import pdb; pdb.set_trace()
            photos = pet.get("photos", [])
            pets.append(cls.build_pet(pet))
        return pets

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
            organization=cls.parse_organization(data.get("organization")),
            contact=cls.parse_contact(data.get("contact")),
        )

    @classmethod
    def parse_organization(self, data: Optional[Dict[str, Any]]) -> Optional[Organization]:
        if not data:
            return None
        return Organization(
            id=str(data.get("id", "unknown")),
            name=data.get("name", "Unknown Organization"),
            address=data.get("address")
        )

    @classmethod
    def parse_contact(cls, data: Optional[Dict[str, Any]]) -> Optional[Contact]:
        if not data:
            return None
        return Contact(
            email=data.get("email"),
            phone=data.get("phone")
        )

