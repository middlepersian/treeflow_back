from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object, connections, Index
from datetime import datetime
import pytest
from time import sleep
from pytest_elasticsearch import factories
from elasticsearch import Elasticsearch
from treeflow.dict.documents.lemma import LemmaDocument
from treeflow.dict.documents.meaning import MeaningDocument
from elasticsearch_dsl import Search, connections


def test_index_lemma_document():

    lemma_doc = LemmaDocument(
        id='2',
        word='2test',
        language='en',
        multiword_expression=False,
        related_lemmas=[
            LemmaDocument(id='2', word='related1', language='en', multiword_expression=False, created_at=datetime.now()),
            LemmaDocument(id='3', word='related2', language='en', multiword_expression=False, created_at=datetime.now())
        ],
        related_meanings=[
            MeaningDocument(id='1', name='meaning1', language='en', created_at=datetime.now()),
            MeaningDocument(id='2', name='meaning2', language='en', created_at=datetime.now())
        ],
        created_at=datetime.now()
    )

    assert lemma_doc.id == '2'
def test_total_count():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    s = Search(index='lemmas')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0    

def test_query_lemmas():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    s = Search(index='lemmas').query('wildcard', word='s*')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print(hit.word)
