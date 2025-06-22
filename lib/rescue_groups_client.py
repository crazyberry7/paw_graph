import os
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()


class RescueGroupsClient:
    BASE_URL = "https://api.rescuegroups.org/v5/public"

    def __init__(self):
        self.api_key = os.getenv("RESCUEGROUPS_API_KEY")
        self.headers = {
            "Authorization": f"apikey {self.api_key}",
            "Content-Type": "application/vnd.api+json"
        }

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def get_animals(
        self,
        species: Optional[str] = None,
        breed: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 25,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        import pdb; pdb.set_trace()
        params = {
            "limit": str(limit),
            "offset": str(offset),
            "sort": "name"
        }

        filters = []

        if species:
            filters.append({
                "fieldName": "species.singular",
                "operation": "equals",
                "criteria": species
            })
        if breed:
            filters.append({
                "fieldName": "breedPrimary",
                "operation": "equals",
                "criteria": breed
            })
        if state:
            filters.append({
                "fieldName": "locationState",
                "operation": "equals",
                "criteria": state
            })

        if filters:
            params["filters"] = {"filter": filters}

        result = await self._get("animals/search", params=params)
        return result.get("data", [])
