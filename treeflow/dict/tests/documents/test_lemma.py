from elasticsearch_dsl import Document, Date, Integer, Boolean, Text, Keyword, Nested, Object, connections, Index
from datetime import datetime
import pytest
from time import sleep
from pytest_elasticsearch import factories
from elasticsearch import Elasticsearch
from treeflow.dict.documents.lemma import LemmaDocument
from treeflow.dict.documents.meaning import MeaningDocument


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

