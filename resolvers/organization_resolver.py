from api.types.types import Organization

class OrganizationResolver:
    @classmethod
    async def resolve(cls, root) -> Organization:
        data = await cls.fetch_organization(root.organization_id)
        return cls.build_organization(data.get("organization"))

    @classmethod
    async def fetch_organization(cls, id: str) -> Organization:
        url = f"https://api.petfinder.com/v2/organizations/{id}"
        res = await PetFinderClient.get(url)
        return res.json()

    @classmethod
    def build_organization(cls, data: Optional[Dict[str, Any]]) -> Optional[Organization]:
        if not data: return None
        return Organization(
            id=str(data.get("id", "unknown")),
            name=data.get("name", "Unknown Organization"),
            address=data.get("address")
        )