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
        __typename
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
    text_faker = TextFactory.create(title="This is a title")

    res = gql_client.query(
        query,
        {
            "input": {
                "title": text_faker.title,
                "textSigle": {"id": to_base64("TextSigle", text_faker.text_sigle.id)},

            }}
    )

    assert res.data == {
        "createText": {
            "title": "This is a text"}
    }

    print(res)
