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
        }

    }
    print(res)


@pytest.mark.django_db(transaction=True)
def test_create_comment(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateComment($input: CommentInput!) {
    createComment(input: $input) {
        ... on  Comment{
        text
        user {
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
    user = UserFactory.create()
    print("USER_FAKER", user, to_base64("User", user.pk))
    res = gql_client.query(
        query,
        {
            "input": {
                "user": {"id": to_base64("User", user.pk)},
                "text": "This is a comment",
            }
        },
    )

    assert res.data == {
        "createComment": {
            "user": {"id": to_base64("User", user.pk)},
            "text": "This is a comment",
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
    text_faker = TextFactory.create()
    print("TEXT_FAKER", text_faker, to_base64("Text", text_faker.pk),  text_faker.text_sigle.id)

    #text_sigle_faker = TextSigleFactory.create()
    #print("TEXT_SIGLE", text_sigle_faker.id, to_base64("TextSigle", text_sigle_faker.id))
    res = gql_client.query(
        query,
        {
            "input": {
                "title": "This is a text",
                "textSigle": {"id": to_base64("TextSigle", text_faker.text_sigle.id)},
            }
        },
    )
    print("RES_DATA", res.data)
    assert res.data == {
        "createText": {
            "title": "This is a text",
            "textSigle": {"id": to_base64("TextSigle",  text_faker.text_sigle.id)},
        }
    }
