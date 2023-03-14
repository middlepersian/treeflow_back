import pytest
from treeflow.corpus.types.text import Text
from treeflow.corpus.tests.utils import GraphQLTestClient
from treeflow.corpus.models import Token, Text
from treeflow.corpus.tests.factories.text import TextFactory
from strawberry_django_plus.relay import from_base64, to_base64
import unicodedata
from django.test.client import Client
from treeflow.corpus.tests.factories.user import UserFactory

@pytest.mark.django_db(transaction=True)
def test_create_token_mutation(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateToken($input: TokenInput!) {
        createToken(input: $input) {
            ... on Token{
                id
                transcription
            }
        }
    }
    """

    ## get the schema

    # Create a Text instance for the Token to belong to
    text = TextFactory()
    # Define the input for the create mutation
    unnormalized_text = "ẞ̌ü̈γēſȟøɯ𝕊" 
    # Test with NFC normalization
    input_data = {
        'text': {"id": to_base64('Text', text.pk)},
        'transcription': unnormalized_text,
    }
    user = UserFactory.create()
    with gql_client.login(user):
        # Execute the mutation
        res = gql_client.query(query, variables={'input': input_data})
        # Assert that the Token was created in the database
        token_id = from_base64(res.data['createToken']['id'])[1]
        assert Token.objects.filter(pk=token_id).exists()
        assert Token.objects.get(pk=token_id).transcription == unicodedata.normalize('NFC', unnormalized_text)

    # Test with NFD normalization
    input_data = {
        'text': {"id": to_base64('Text', text.pk)},
        'transcription': unnormalized_text,
    }
    user = UserFactory.create()
    with gql_client.login(user):
        # Execute the mutation
        res = gql_client.query(query, variables={'input': input_data})
        # Assert that the Token was created in the database
        token_id = from_base64(res.data['createToken']['id'])[1]
        assert Token.objects.filter(pk=token_id).exists()
        assert Token.objects.get(pk=token_id).transcription == unicodedata.normalize('NFD', unnormalized_text)


@pytest.mark.django_db(transaction=True)
def test_normalize_trans(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateToken($input: TokenInput!) {
        createToken(input: $input) {
            ... on Token{
                id
                transcription
            }
        }
    }
    """

    # Create a Text instance for the Token to belong to
    text = TextFactory()

    # Define the input for the create mutation
    unnormalized_text = "âbcde"  # Use the composed character "â" (U+00E2)

    nfd_normalized = unicodedata.normalize('NFD', unnormalized_text)
    nfc_normalized = unicodedata.normalize('NFC', unnormalized_text)

    # Test with NFC normalization
    input_data = {
        'text': {"id": to_base64('Text', text.pk)},
        'transcription': nfd_normalized,
    }
    user = UserFactory.create()
    with gql_client.login(user):
        # Execute the mutation
        res = gql_client.query(query, variables={'input': input_data})
        # Assert that the Token was created in the database
        token_id = from_base64(res.data['createToken']['id'])[1]
        assert Token.objects.filter(pk=token_id).exists()
        assert Token.objects.get(pk=token_id).transcription == nfd_normalized



@pytest.mark.django_db(transaction=True)
def test_create_text_mutation(db, gql_client: GraphQLTestClient):
    query = """
    mutation CreateText($input: TextInput!) {
        createText(input: $input) {
            __typename
            ... on Text {
                id
                title
            }
            ... on OperationInfo {
                messages {
                    kind
                    field
                    message
                }
            }
        }
    }
    """

    # Define the input for the create mutation
    title = "Test Text"
    input_data = {
        'title': title,
    }
    user = UserFactory.create()
    with gql_client.login(user):
        # Execute the mutation
        res = gql_client.query(query, variables={'input': input_data})

        # Assert the response has no errors
        assert res.errors is None

        # Assert the response contains a Text instance or an OperationInfo with a message
        assert res.data['createText']['__typename'] in ['Text', 'OperationInfo']
        if res.data['createText']['__typename'] == 'Text':
            # Assert the Text instance has the correct title
            assert res.data['createText']['title'] == title
        else:
            # Assert the OperationInfo has a message with the error
            assert res.data['createText']['messages'][0]['kind'] == 'error'
        # Assert that the Text was created in the database
        text_id = from_base64(res.data['createText']['id'])[1]
        assert Text.objects.filter(pk=text_id).exists()
        assert Text.objects.get(pk=text_id).title == title
