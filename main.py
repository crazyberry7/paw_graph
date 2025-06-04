import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from api.schema import schema

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

