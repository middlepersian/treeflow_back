import pytest

from mpcd.corpus.models import Comment
from .faker import CommentFactory
from .utils import GraphQLTestClient, assert_num_queries


@pytest.mark.django_db(transaction=True)
def test_input_mutation(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateComment ($input: CreateCommentInput!) {
        createComment (input: $input) {
            text
        }
      }
    """
    with assert_num_queries(1):
        res = gql_client.query(
            query,
            {
                "input": {
                    "text": "Hello world",
                }
            },
        )
        assert res.data == {
            "createComment": {
                "text": "Hello world",
            }
        }
