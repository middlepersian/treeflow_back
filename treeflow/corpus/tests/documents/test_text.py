import pytest
from elasticsearch_dsl import Search, connections

connections.create_connection(hosts=['elastic:9200'], timeout=20)




def test_total_count():
    s = Search(index='text')
    response = s.execute()
    total_count = response.hits.total.value
    print('total_count', total_count)
    for hit in response[:10]:
        print(hit.id, hit.title, hit.language, hit.created_at)