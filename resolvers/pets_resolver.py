from typing import *
from lib import *
from api.types.types import Pet, Contact  # Assuming these are defined in types.py

class PetsResolver:
    """Responsible for transforming raw API data into Pet objects."""

    @classmethod
    async def resolve(cls, location, type, limit) -> list[Pet]:
        url = f"https://api.petfinder.com/v2/animals?location={location}&type={type.capitalize()}&limit={limit}"
        res = await PetFinderClient.get(url)
        return list(map(cls.build_pet, res.get("animals", [])))

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
            organization_id=data.get("organization_id"),
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

