
from elasticsearch_dsl import Search, connections, Q
from treeflow.dict.types.meaning import MeaningElastic



def test_total_count():
    s = Search(index='lemmas')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0    

def test_query_meanings():
    s = Search(index='meanings').query('wildcard', meaning='s*')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    assert total_count > 0

    for hit in response[:10]:
        print(hit.id, hit.meaning, hit.language)

   
def test_parse_hits():
    pattern = 'gött*'
    query_type = 'match'
    size = 10
    s = Search(index='meanings').query(Q(query_type, meaning=pattern)).extra(size=size)
    response = s.execute()

    meanings = []
    for hit in response.hits.hits:
        meaning = MeaningElastic.from_hit(hit)
        meanings.append(meaning)
    print(meanings)