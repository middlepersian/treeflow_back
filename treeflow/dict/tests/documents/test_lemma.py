from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object, connections, Index
from datetime import datetime
import pytest
from time import sleep
from pytest_elasticsearch import factories
from elasticsearch import Elasticsearch
from treeflow.dict.documents.lemma import LemmaDocument
from treeflow.dict.documents.meaning import MeaningDocument
from elasticsearch_dsl import Search, connections
import asyncio
from elasticsearch import AsyncElasticsearch
from treeflow.dict.types.lemma import LemmaElastic
from typing import List
from strawberry_django_plus.gql import relay

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
        print(hit.id, hit.word, hit.language, hit.created_at, hit.related_lemmas, hit.related_meanings)
        
    lemmas_elastic = resolve_lemmas(response)
    for lemma in lemmas_elastic:
        print(lemma.id, lemma.word, lemma.language, lemma.created_at, lemma.related_lemmas, lemma.related_meanings)


def resolve_lemmas(lemmas) -> List[LemmaElastic]:
    lemmas_elastic = []
    for lemma in lemmas:
        lemma_elastic = LemmaElastic(id=lemma.id, word=lemma.word, language=lemma.language, multiword_expression=lemma.multiword_expression, created_at=lemma.created_at, related_lemmas=lemma.related_lemmas, related_meanings=lemma.related_meanings)
        lemmas_elastic.append(lemma_elastic)
    return lemmas_elastic    



def test_query_meanings():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    s = Search(index='meanings').query('wildcard', meaning='s*')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print(hit.id, hit.meaning, hit.language, hit.created_at )


def test_simple_lemma_query():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    s = Search(index='lemmas').query('wildcard', word='*as')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print( hit.id, hit.word, hit.language, hit.created_at, hit.related_lemmas, hit.related_meanings)

def test_get_lemmas_by_id():
    connections.create_connection(hosts=['elastic:9200'], timeout=20)
    ids = ['7a380bce-e3fe-42af-b106-28c197d77d31']
    s = Search(index='lemmas').query('ids', values=ids)
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    for hit in response[:10]:
        print( hit.id, hit.word, hit.language, hit.created_at, hit.related_lemmas, hit.related_meanings)        