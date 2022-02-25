from fastapi.testclient import TestClient

from api_elasticsearch import api

client = TestClient(api)


url_no_index = "http://localhost:8000/search?query={query}&field={field}"
url = url_no_index + "&index={index}"


def test_index():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "running"}


def test_info():
    resp = client.get("/info")
    assert resp.status_code == 200
    assert resp.json()["indexes"] != {}


def test_search_with_wrong_index():
    resp = client.get(
        url.format(query="great", field="customer_reviews", index="wrong_index")
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Index wrong_index does not exist"}


def test_search_with_no_index():
    resp = client.get(
        url_no_index.format(query="great", field="customer_reviews")
    )
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_search_with_existing_index():
    resp = client.get(
        url.format(query="great", field="customer_reviews", index="amazon")
    )
    assert resp.status_code == 200
    assert len(resp.json()) > 0


def test_search_with_bad_query():
    resp = client.get(
        url.format(query="bbbbbbbb", field="customer_reviews", index="*")
    )
    assert resp.status_code == 200
    assert len(resp.json()["results"]["hits"]["hits"]) == 0


def test_search_with_correct_query():
    resp = client.get(
        url.format(query="the", field="customer_reviews", index="*")
    )
    assert resp.status_code == 200
    assert len(resp.json()["results"]["hits"]["hits"]) > 0
