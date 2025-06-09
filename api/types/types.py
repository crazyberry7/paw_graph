import strawberry
from typing import *
from lib.pet_finder_client import PetFinderClient

@strawberry.type
class Contact:
    email: Optional[str]
    phone: Optional[str]

@strawberry.type
class Organization:
    id: strawberry.ID
    name: str
    address: str
    email: Optional[str] = None
    phone: Optional[str] = None

class OrganizationResolver:
    @classmethod
    async def resolve(cls, root) -> Organization:
        url = f"https://api.petfinder.com/v2/organizations/{root.organization_id}"
        data = await PetFinderClient.get(url)
        return cls.build_organization(data.get("organization"))

    @classmethod
    def build_organization(cls, data: Optional[Dict[str, Any]]) -> Optional[Organization]:
        if not data: return None
        return Organization(
            id=str(data.get("id", "unknown")),
            name=data.get("name", "Unknown Organization"),
            address=cls.__build_address(data.get("address"))
        )

    @classmethod
    def __build_address(cls, data: Optional[Dict[str, Any]]) -> Optional[str]:
        if not data: return ""
        return ' '.join(str(v) for v in data.values() if v is not None)

@strawberry.type
class Pet:
    id: strawberry.ID
    name: str
    breed: str
    age: Optional[str]
    gender: str
    description: Optional[str]
    photo: Optional[str]
    organization_id: Optional[strawberry.ID]
    organization: Optional[Organization] = strawberry.field(resolver=OrganizationResolver.resolve)
    contact: Optional[Contact]


