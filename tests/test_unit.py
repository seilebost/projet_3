from fastapi.testclient import TestClient
import pytest
from elasticsearch import Elasticsearch
import json
import os
from collections import namedtuple


from api_elasticsearch import api

client = TestClient(api)

TEST_INDEX = "test_index"


url_no_index = "/search?query={query}&field={field}"
url = url_no_index + "&index={index}"

es = Elasticsearch("http://localhost:9200")


def get_test_data():
    """
    Return test data from JSON file
    """
    with open(f"{os.getcwd()}/tests/test_data.json") as data_file:
        data = json.load(data_file)

    test_tuple = namedtuple(typename="test", field_names=list(data.keys()))

    data_dict = {}
    for key in data.keys():
        data_dict[key] = namedtuple(
            typename="test_data", field_names=list(data[key].keys())
        )(**data[key])

    return test_tuple(**data_dict)


test_data = get_test_data()


def setup_module(module):
    """Create an index for test purposing"""

    with open(f"{os.getcwd()}/mapping.json") as mapping:
        dict_mapping = json.load(mapping)

    es.indices.create(index=TEST_INDEX, body=dict_mapping)


def teardown_module(module):
    """Delete the test index"""
    es.indices.delete(index=TEST_INDEX)


def test_index():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "running"}


def test_info():
    resp = client.get("/info")
    assert resp.status_code == 200
    assert resp.json()["indexes"] != {}
    assert TEST_INDEX in resp.json()["indexes"].keys()


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


class TestWithDocuments:
    @classmethod
    def setup_class(cls):
        """
        Add documents to test index for the methods
        """
        cls.es = Elasticsearch("http://localhost:9200")

        cls.es.index(
            index=TEST_INDEX,
            body=test_data.GoodProduct._asdict(),
            refresh="wait_for",
        )

        cls.es.index(
            index=TEST_INDEX,
            body=test_data.BadProduct._asdict(),
            refresh="wait_for",
        )

    def test_count(self):

        resp = client.get(f"/count?index={TEST_INDEX}")

        assert resp.status_code == 200
        assert isinstance(resp.json()["count"], int)
        assert resp.json()["count"] == len(test_data)

    @pytest.mark.parametrize("wrong", ["&outputs=", "&outputs=wrong"])
    def test_search_wrong_outputs(self, wrong):
        resp = client.get(
            (url + wrong).format(
                query="great", field="description", index=TEST_INDEX
            )
        )

        assert resp.status_code == 200
        assert resp.json()["results"]["hits"]["hits"][0]["_source"] == {}

    def test_search_outputs(self):

        resp = client.get(
            (url + "&outputs=product_name&outputs=description").format(
                query=test_data.GoodProduct.description,
                field="description",
                index=TEST_INDEX,
            )
        )

        assert resp.status_code == 200
        assert list(
            resp.json()["results"]["hits"]["hits"][0]["_source"].keys()
        ) == ["description", "product_name"]

    def test_search_with_correct_query(self):
        resp = client.get(
            url.format(
                query=test_data.GoodProduct.product_name,
                field="product_name",
                index=TEST_INDEX,
            )
        )
        assert resp.status_code == 200
        assert len(resp.json()["results"]["hits"]["hits"]) > 0

    def test_search_with_bad_query(self):
        resp = client.get(
            url.format(
                query="bbbbbbbb", field="customer_reviews", index=TEST_INDEX
            )
        )
        assert resp.status_code == 200
        assert len(resp.json()["results"]["hits"]["hits"]) == 0

    def test_search_with_existing_index(self):
        resp = client.get(
            url.format(
                query="great", field="customer_reviews", index=TEST_INDEX
            )
        )
        assert resp.status_code == 200
        assert len(resp.json()) > 0
