from typing import List

import strawberry
from api.types.types import Pet
from resolvers.adoptable_pets_resolver import AdoptablePetsResolver

@strawberry.type
class Query:
    """GraphQL Query class to define the entry points for the API."""
    @strawberry.field
    async def adoptable_pets(self, info: strawberry.Info,
                             source: str,
                             location: str,
                             distance: int = 100,
                             type: str = "Dog",
                             limit: int = 5) -> List[Pet]:
        clients = {
            "pf": info.context["pf_client"],
            "rg": info.context["rg_client"]
        }
        client = clients.get(source)
        if not client: raise ValueError("Invalid source specified. Use 'pf' or 'rg'.")
        return await AdoptablePetsResolver(client).resolve(location, type, limit)