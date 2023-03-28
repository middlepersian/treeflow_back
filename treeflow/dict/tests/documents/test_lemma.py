from datetime import datetime
import os
import pytest
from treeflow.dict.models.lemma import Lemma as LemmaModel
from treeflow.dict.documents.lemma import LemmaDocument
from treeflow.dict.documents.meaning import MeaningDocument
from elasticsearch_dsl import Search, Q
from treeflow.dict.types.lemma import LemmaElastic
from typing import List
from strawberry_django_plus.gql import relay
from unittest.mock import patch
# import django settings
from django.conf import settings

from treeflow.schema import schema




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
    s = Search(index='lemmas')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0    

def test_query_lemmas():
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
    s = Search(index='meanings').query('wildcard', meaning='s*')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print(hit.id, hit.meaning, hit.language, hit.created_at )


def test_simple_lemma_query():
    s = Search(index='lemmas').query('prefix', word='a')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0
    for hit in response[:10]:
        print( hit.id, hit.word, hit.language, hit.created_at, hit.related_lemmas, hit.related_meanings)

def test_get_lemmas_by_id():
    ids = ['7a380bce-e3fe-42af-b106-28c197d77d31']
    s = Search(index='lemmas').query('ids', values=ids)
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    for hit in response[:10]:
        print( hit.id, hit.word, hit.language, hit.created_at, hit.related_lemmas, hit.related_meanings)        


def test_get_lemmas_by_wildcard():
    # create a new search object and add the query
    s = Search(index='lemmas').query('wildcard', word="*a")

    # execute the search and retrieve the results
    response = s.execute()

    print(response.hits.total.value)

    # extract the relevant data from the search hits and return as a list of dictionaries
    lemmas = []
    for hit in response.hits.hits:
        lemma = {
            'id': hit['_id'],
            'word': hit['_source']['word'],
            'language': hit['_source']['language'],
            'multiword_expression': hit['_source']['multiword_expression'],
            'created_at': hit['_source']['created_at'],
        }
        lemmas.append(lemma)

    print(lemmas)     

    return lemmas



def test_resolve_node():
    # Create a dummy LemmaElastic object to use for testing
    lemma = LemmaElastic(
        id=relay.to_base64("LemmaElastic", "abc123"),
        word="test",
        language="en",
        multiword_expression=False,
        created_at=datetime.now(),
    )
    # Mock the get_lemma_by_id function to return the dummy object
    with patch("treeflow.dict.types.lemma.get_lemma_by_id", return_value=lemma):
        # Call the resolver with a valid node_id
        result = LemmaElastic.resolve_node(node_id=lemma.id)
        # Assert that the returned object matches the dummy object
        assert result == lemma

def test_global_id():
    # Test resolve_node with specific global ID
    # Create a dummy LemmaElastic object to use for testing
    lemma = LemmaElastic(
        id="TGVtbWFFbGFzdGljOjBlODUzZTY1LTMyZTktNGY5OS1iZDBlLTdlZjEzMjBkNTkxNA==", # Global ID
        word="test",
        language="en",
        multiword_expression=False,
        created_at=datetime.now(),
    )

    # Call the resolver with the global ID of the dummy object
    global_id = relay.to_base64("LemmaElastic", str(lemma.id))
    try:
        # Call resolve_node with global ID
        node = LemmaElastic.resolve_node(node_id=global_id)

        # Ensure node is not None
        assert node is not None

        # Ensure node has the correct ID
        assert node.id == global_id
    except Exception as e:
        print(e)
        raise


def test_solve_ids():
    # Test resolve_node with specific global ID
    gid ="TGVtbWFFbGFzdGljOjBlODUzZTY1LTMyZTktNGY5OS1iZDBlLTdlZjEzMjBkNTkxNA=="
    print(gid)
    # solve it as a global id
    global_id = relay.from_base64(gid)
    print(global_id)
    print(global_id[0])
    print(global_id[1])
    node = LemmaElastic.resolve_node(gid)
    print('node', node)
    print('node.id', node.id)

def test_resolve_id():
    # Create a mock instance of LemmaElastic
    lemma = LemmaElastic(
        id='TGVtbWFFcnN0aWNhbDoxcQ==',
        word='test',
        language='en',
        multiword_expression=False,
        created_at='2022-01-01T00:00:00',
    )

    # Call the resolve_id method of the LemmaElastic class
    resolved_id = LemmaElastic.resolve_id(lemma)
    print('resolved_id',resolved_id)

    # Assert that the resolved ID matches the expected value
    assert resolved_id == 'TGVtbWFFcnN0aWNhbDoxcQ=='

def test_node_id():
    node_id = "TGVtbWFFbGFzdGljOjBlODUzZTY1LTMyZTktNGY5OS1iZDBlLTdlZjEzMjBkNTkxNA=="
    expected_id = "LemmaElastic:0e853e65-32e9-4f99-bd0e-7ef1320d5914"

    # Check that node_id matches the expected value
    assert node_id == relay.to_base64("LemmaElastic", "0e853e65-32e9-4f99-bd0e-7ef1320d5914")

    # Decode the node ID and check that it matches the expected value
    decoded_id = relay.from_base64(node_id)
    assert decoded_id == ("LemmaElastic", "0e853e65-32e9-4f99-bd0e-7ef1320d5914")

    # Check that the decoded node ID matches the expected value
    assert ":".join(decoded_id) == expected_id
   


def test_my_query():
    result = schema.execute_sync(
        """
        query TestQuery ($id: GlobalID!) {
            node (id: $id) {
                ... on LemmaElastic {
                    id
                    word
                }
            }
        }
        """,
        variable_values={
            "id": relay.to_base64("LemmaElastic", 1)
        },
    )
    assert result.errors is None
    assert result.data == {
        "node":{
                "id": relay.to_base64("LemmaElastic", 1),
                "word": "example_word_1",
            }
            } 



@pytest.fixture
def lemma_elastic_instance():
    # Create a LemmaElastic instance with a known ID
    return LemmaElastic(
        id="TGVtbWFFbGFzdGljOjNmZTI5ODYxLTUzMjAtNDY3Yi04MDdjLTA5MWQ1NzgyZDQ3Mg==",
        word="eieieie",
        language="spa",
        multiword_expression=False,
        created_at=datetime.now(),
        lemma="some_lemma_id"
    )





@pytest.fixture
def lemma(db):
    return LemmaModel.objects.create(
        word="test",
        language="eng",
        multiword_expression=False,
    )


def test_resolve_lemma(lemma):
    lemma_elastic = LemmaElastic(
        id="TGVtbWFFbGFzdGljOjNmZTI5ODYxLTUzMjAtNDY3Yi04MDdjLTA5MWQ1NzgyZDQ3Mg==",
        word="test",
        language="ENGLISH",
        multiword_expression=False,
        created_at="2022-01-01T00:00:00",
    )
    lemma_elastic.lemma = lemma

    resolved_lemma = lemma_elastic.resolve_lemma("TGVtbWFFbGFzdGljOjNmZTI5ODYxLTUzMjAtNDY3Yi04MDdjLTA5MWQ1NzgyZDQ3Mg==")

    assert resolved_lemma.id == str(lemma.id)
    assert resolved_lemma.word == lemma.word
    assert resolved_lemma.language == lemma.language
    assert resolved_lemma.multiword_expression == lemma.multiword_expression


def test_lemma_document():
    id = "TGVtbWFFbGFzdGljOjU0ZDIwMjkyLTkxZWYtNDMxZi1hMjQxLWJiMDUzZTYzNzFhZg=="
    q = Q('ids', values=[id])
    lemma = LemmaDocument.search().query(q).execute()
    print(lemma.to_dict())

def test_lemma_search():
    query_type = "wildcard"
    pattern = "*da*"
    size = 20
    q = Q(query_type, word=pattern)
    response =LemmaDocument.search().query(q).extra(size=size)

    lemmas = []
    for hit in response:
        lemma = LemmaElastic.from_hit(hit)
        lemmas.append(lemma)
    print(lemmas)
    return lemmas