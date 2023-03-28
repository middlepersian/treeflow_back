
from treeflow.corpus.documents.token import TokenDocument
from treeflow.corpus.types.token import TokenElastic
import pytest
from elasticsearch_dsl import Search, Q


@pytest.mark.django_db
def test_get_queryset():
    qs = TokenDocument().get_queryset()
    assert qs.count() == 0

def test_total_count():
    s = Search(index='tokens')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    for hit in response[:10]:
        print(hit.id, hit.title, hit.language, hit.created_at)


def test_token_search():
    
    # Define the search query
    prev_transcription_query = Q('nested', path='previous', query=Q('match', previous__transcription='frahang'))
    current_transcription_query = Q('match', transcription='dēn')
    pos_query = Q('nested', path='pos_token', query=Q('match', pos_token__pos='NOUN'))
    q = prev_transcription_query & current_transcription_query & pos_query


    # Perform the search
    response = TokenDocument.search().query(q)

    print('response', response)

    # Print the results
    for hit in response:
        print(hit.transcription, hit.previous.transcription, hit.pos_token, hit.feature_token)


def test_search():
        query_type = 'wildcard'
        pattern = 'pad*'
        q = Q(query_type, transcription=pattern)
        size = 100
        response = TokenDocument.search().query(q).extra(size=size)

        tokens = []
        for hit in response:
            print(hit.transcription, hit.previous.transcription, hit.pos_token, hit.feature_token)
            
            token = TokenElastic.from_hit(hit)
            tokens.append(token)

        return tokens