import pytest
from strawberry_django_plus.relay import from_base64, to_base64

from .utils import GraphQLTestClient, assert_num_queries
from .faker import(UserFactory, TextFactory, TextSigleFactory)


@pytest.mark.django_db(transaction=True)
def test_create_text_sigle(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateTextSigle($input: TextSigleInput!) {
    createTextSigle(input: $input) {
        ... on  TextSigle{
        sigle
        genre
        }
        ... on OperationInfo{
        messages{
            kind
            message
            field
        }
        }
    }
    }
    """
    res = gql_client.query(
        query,
        {
            "input": {
                "sigle": "LOVE",
                "genre": "POE",
            }
        },
    )

    assert res.data == {
        "createTextSigle": {
            "sigle": "LOVE",
            "genre": "POE"
        }

    }
    print(res)




@pytest.mark.django_db(transaction=True)
def test_create_text(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateText($input: TextInput!) {
    createText(input: $input) {
        ... on  Text{
        title
        textSigle {
            id
        }
        }
        ... on OperationInfo{
        messages{
            kind
            message
            field
        }
        }
    }
    }
    """
    text_sigle_faker = TextSigleFactory.create(sigle="LOVE", genre="POE")
    # text_faker = TextFactory.create(title="This is a title")

    res = gql_client.query(
        query,
        {
            "input": {
                "title": "This is a text",
                "textSigle": {"id": to_base64("TextSigle", text_sigle_faker.id)},

            }}
    )

    assert res.data == {
        "createText": {
            "title": "This is a text",
            "textSigle": {"id": to_base64("TextSigle", text_sigle_faker.id)}}
    }

    print(res)
