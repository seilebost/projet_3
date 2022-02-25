from fastapi import FastAPI, HTTPException
import uvicorn
from elasticsearch import Elasticsearch
from typing import Optional

api = FastAPI(
    title="API Elasticsearch",
    description="""This API allow to access an Elasticsearch database
    """,
    version="1.0.0",
)

# Connect to Elasticsearch
client = Elasticsearch("http://localhost:9200")


@api.get("/", name="Check API")
def index() -> dict:
    """
    Return a dictionnary that indicate the api is running
    """

    return {"status": "running"}


@api.get("/info", name="Get index informations")
def get_info() -> dict:
    """
    Return informations on indexes in database
    """

    return {"indexes": client.indices.get(index="*")}


@api.get("/search", name="Search for documents")
def search(query, field, index: Optional[str] = "*") -> dict:
    """
    Return documents according to search query
    """

    if index != "*" and index not in client.indices.get(index="*").keys():
        raise HTTPException(
            status_code=404, detail=f"Index {index} does not exist"
        )

    return {
        "results": client.search(
            index=index, body={"query": {"match": {field: query}}}
        )
    }


if __name__ == "__main__":
    uvicorn.run(
        "api_elasticsearch:api",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
