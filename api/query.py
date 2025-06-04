from typing import List

import strawberry
from api.types.types import Pet
from resolvers.pet_resolver import PetResolver

@strawberry.type
class Query:
    @strawberry.field
    async def adoptable_pets(self, location: str, distance: int = 100, type: str = "Dog", limit: int = 5) -> List[Pet]:
        return await PetResolver.fetch_pets(location, type, limit)