import pytest
from elasticsearch_dsl import connections
from treeflow.corpus.documents import TokenDocument
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
## we will make a query to get all tokens starting with the letter 'a'
def test_token_document():

    connections.create_connection(hosts=['elastic:9200'], timeout=20)

    s = Search(index='tokens').query('wildcard', transcription='an*')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print(hit.transcription)