import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from api.schema import schema
from lib import *


async def context_getter():
    return {
        "pf_client": PetFinderClient,
        "rg_client": RescueGroupsClient
    }

graphql_app = GraphQLRouter(schema, context_getter=context_getter)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

