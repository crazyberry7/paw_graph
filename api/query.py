from typing import List

import strawberry
from api.types.types import Pet
from resolvers.pets_resolver import PetsResolver

@strawberry.type
class Query:
    @strawberry.field
    async def adoptable_pets(self, location: str, distance: int = 100, type: str = "Dog", limit: int = 5) -> List[Pet]:
        return await PetsResolver.resolve(location, type, limit)