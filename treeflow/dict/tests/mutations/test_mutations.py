import json
import pytest
from treeflow.users.models import User
from treeflow.dict.models import Lemma, Meaning 
from treeflow.dict.types import Lemma as LemmaType
from treeflow.dict.types import Meaning as MeaningType
from strawberry_django.test.client import TestClient
from strawberry import relay


@pytest.fixture
def user(db):
    user = User.objects.create(username='fco', password='test')
    return user
    
@pytest.fixture
def lemma(db):
    return Lemma.objects.create(word='haus', language='en') 

@pytest.fixture
def meaning(db):
    return Meaning.objects.create(meaning='place to live', language='en')


# Write a simple test to use the fixtures
def test_fixture_user(db, user):
    assert User.objects.count() == 1
    assert user.username == 'fco'

def test_fixture_lemma(db, lemma):
    assert Lemma.objects.count() == 1
    # Add any additional assertions to verify the lemma object

def test_fixture_meaning(db, meaning):
    assert Meaning.objects.count() == 1
    # Add any additional assertions to verify the meaning object    


# Tests
def test_add_related_meaning_unauthenticated(db, lemma, meaning):
    client = TestClient("/graphql")
    lemma_id = relay.to_base64(LemmaType, lemma.id)  # Convert to GlobalID
    meaning_id = relay.to_base64(MeaningType, meaning.id)  # Convert to GlobalID
    query = f"""
        mutation {{
            addRelatedMeaningToLemma(input: {{ lemma: "{lemma_id}", relatedMeaning: "{meaning_id}" }}) {{
                lemma {{
                    id
                }}
            }}
        }}
    """
    res = client.query(query)
    assert "errors" in res
    assert res["errors"][0]["message"] == "You must be authenticated for this operation."


def test_add_related_meaning_invalid_input(db, user, lemma):
    client = TestClient("/graphql")
    lemma_id = relay.to_base64(LemmaType, lemma.id)  # Convert to GlobalID
    query = f"""
        mutation {{
            addNewRelatedMeaningToLemma(input: {{ lemma: "{lemma_id}", relatedMeanings: {{ meaning: "test meaning", language: "de", relatedMeanings: [] }} }}) {{                
                lemma {{
                    id
                    word
                    relatedMeanings {{
                        id 
                        meaning
                        language
                }}
            }}
        }}
    """

    res = client.query(query)
    assert "errors" in res
    # Add any additional assertions based on your validation logic

def test_add_related_meaning_valid_input(db, user, lemma):
    client = TestClient("/graphql")
    lemma_id = relay.to_base64(LemmaType, lemma.id)  # Convert to GlobalID
    query = f"""
        mutation {{
            addNewRelatedMeaningToLemma(input: {{ lemma: "{lemma_id}", relatedMeanings: {{ meaning: "test meaning", language: "de" }} }}) {{                
                lemma {{
                    id
                    word
                    relatedMeanings {{
                        id 
                        meaning
                        language
                }}
            }}
        }}
    """
    res = client.query(query)
    assert "errors" not in res
    assert "lemma" in res["data"]["addNewRelatedMeaningToLemma"]
    # Add any additional assertions based on your validation logic    