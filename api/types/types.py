import strawberry
from typing import Optional

from resolvers.organization_resolver import OrganizationResolver


@strawberry.type
class Contact:
    email: Optional[str]
    phone: Optional[str]

@strawberry.type
class Organization:
    id: strawberry.ID
    name: str
    email: Optional[str]
    phone: Optional[str]

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
