from elasticsearch_dsl.connections import add_connection, connections
from unittest.mock import Mock
from pytest import fixture, skip


@fixture
def mock_client(dummy_response):
    client = Mock()
    client.search.return_value = dummy_response
    add_connection("mock", client)
    yield client
    connections._conn = {}
    connections._kwargs = {}


@fixture
def dummy_response():
    return {
        "_shards": {"failed": 0, "successful": 10, "total": 10},
        "hits": {
            "hits": [
                {
                    "_index": "test-index",
                    "_type": "company",
                    "_id": "elasticsearch",
                    "_score": 12.0,
                    "_source": {"city": "Amsterdam", "name": "Elasticsearch"},
                },
                {
                    "_index": "test-index",
                    "_type": "employee",
                    "_id": "42",
                    "_score": 11.123,
                    "_routing": "elasticsearch",
                    "_source": {
                        "name": {"first": "Shay", "last": "Bannon"},
                        "lang": "java",
                        "twitter": "kimchy",
                    },
                },
                {
                    "_index": "test-index",
                    "_type": "employee",
                    "_id": "47",
                    "_score": 1,
                    "_routing": "elasticsearch",
                    "_source": {
                        "name": {"first": "Honza", "last": "Král"},
                        "lang": "python",
                        "twitter": "honzakral",
                    },
                },
                {
                    "_index": "test-index",
                    "_type": "employee",
                    "_id": "53",
                    "_score": 16.0,
                    "_routing": "elasticsearch",
                },
            ],
            "max_score": 12.0,
            "total": 123,
        },
        "timed_out": False,
        "took": 123,
    }
