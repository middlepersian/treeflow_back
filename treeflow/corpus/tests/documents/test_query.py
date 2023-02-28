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

    print()

    '''
    for hit in response[:10]:
        print(hit.number)
        print(hit.transcription)
        print([x.pos for x in hit.pos_token])
        print([x.feature for x in hit.feature_token])
        print([x.feature_value for x in hit.feature_token])
        print([x.rel for x in hit.dependency_token])
        print(hit.previous.number, hit.previous.transcription) 
        print(hit.next.number, hit.next.transcription)
    '''    

def test_total_count():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    s = Search(index='tokens')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0

