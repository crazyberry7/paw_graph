import strawberry
from enum import Enum
from typing import Optional

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
    organization: Optional[Organization]
    contact: Optional[Contact]

@strawberry.enum
class Source(Enum):
    PETFINDER = "petfinder"
    RESCUEGROUPS = "rescuegroups"

