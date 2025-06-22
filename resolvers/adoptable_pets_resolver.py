from typing import *
from lib import *
from api.types.types import Pet, Contact  # Assuming these are defined in types.py

class AdoptablePetsResolver:
    """Responsible for transforming raw API data into Pet objects."""
    def __init__(self, client):
        self.client = client

    async def resolve(self, location, type, limit) -> list[Pet]:
        import pdb; pdb.set_trace()
        params = {"location": location, "type": type.capitalize(), "limit": limit}
        pets = await self.client.get_adoptable_pets(params)
        return list(map(self.build_pet, pets))

    def build_pet(self, data: Dict[str, Any]) -> Pet:
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
            contact=self.parse_contact(data.get("contact")),
        )

    def parse_contact(self, data: Optional[Dict[str, Any]]) -> Optional[Contact]:
        if not data:
            return None
        return Contact(
            email=data.get("email"),
            phone=data.get("phone")
        )

