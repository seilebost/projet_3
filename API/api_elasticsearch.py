from fastapi import FastAPI, HTTPException, Query
import uvicorn
from elasticsearch import Elasticsearch
from typing import Optional, List
from pydantic import BaseModel, Field
import os

api = FastAPI(
    title="API Elasticsearch",
    description="""This API allow to access an Elasticsearch database
    """,
    version="1.0.0",
)


# Get elastic instance from environment
ELASTIC_URL = os.getenv("ELASTIC_URL", "localhost:9200")

# Connect to Elasticsearch
client = Elasticsearch(ELASTIC_URL)


class Document(BaseModel):
    """
    Define fields available for a document
    """

    amazon_category_and_sub_category: Optional[str] = None
    average_review_rating: Optional[float] = Field(None, gt=0)
    customer_questions_and_answers: Optional[str] = None
    customer_reviews: Optional[str] = None
    customers_who_bought_this_item_also_bought: Optional[str] = None
    description: Optional[str] = None
    items_customers_buy_after_viewing_this_item: Optional[str] = None
    manufacturer: str
    number_available_in_stock: Optional[str] = None
    number_of_answered_questions: Optional[int] = Field(None, gt=0)
    number_of_reviews: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    product_description: Optional[str] = None
    product_information: Optional[str] = None
    product_name: str
    sellers: Optional[str] = None


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
def search(
    query,
    field,
    outputs: Optional[List[str]] = Query(
        None,
        title="Outputs fields",
        description="Filter the fields returned by the query",
    ),
    index: Optional[str] = "*",
) -> dict:
    """
    Return documents according to search query
    """

    if index != "*" and index not in client.indices.get(index="*").keys():
        raise HTTPException(
            status_code=404, detail=f"Index {index} does not exist"
        )

    body = {"query": {"match": {field: query}}}

    if outputs:
        body["_source"] = outputs

    return {
        "results": client.search(
            index=index,
            body=body,
        )
    }


@api.get("/count", name="Count documents")
def count(
    index: Optional[str] = "*",
    q: Optional[str] = Query(
        None,
        name="Query string",
        description="Query in the Lucene query string syntax",
    ),
) -> dict:
    """
    Return the count of documents according to indexes and query
    """

    return {"count": client.count(index=index, q=q)["count"]}


@api.post("/create_document/{index}", name="Create a new Document in index")
def create_document(index, document: Document) -> dict:
    """
    Add a new document to the given index with data from body request
    """

    # With the refresh parameter the server's response will be delayed until
    # Elasticsearch has update the index
    return client.index(index=index, body=document.dict(), refresh="wait_for")


if __name__ == "__main__":
    uvicorn.run(
        "api_elasticsearch:api",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
