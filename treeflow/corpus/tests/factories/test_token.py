import pytest
from treeflow.corpus.models import Token
from treeflow.corpus.tests.factories import TokenFactory, TextFactory


@pytest.mark.django_db
def test_token_factory():
    """Test token factory"""
    token = TokenFactory()
    assert isinstance(token, Token)

    assert token.number
    assert token.root == False
    assert token.word_token
    assert token.visible
    assert token.text
    assert token.language
    assert token.transcription
    assert token.transliteration
    assert token.avestan
    assert token.gloss


    previous = TokenFactory()
    token.previous = previous
    assert isinstance(token.previous, Token)



@pytest.mark.django_db
def test_insert_token_logic():
    # Create a text to associate tokens with
    text = TextFactory() # Assuming you have a factory for creating Text instances

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2
    token2.previous = token1
    token2.next = token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()


@pytest.mark.django_db
def test_next_previous():
    # Create a text to associate tokens with
    text = TextFactory()

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2
    token2.previous = token1
    token2.next = token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()

    # Check that the tokens were linked correctly
    assert token1.next == token2
    assert token2.previous == token1
    assert token2.next == token3
    assert token3.previous == token2


@pytest.mark.django_db
def test_insert_before():
    # Create a text to associate tokens with
    text = TextFactory()

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2
    token2.previous = token1
    token2.next = token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()

    # Insert a new token before token2
    new_token_data = {'transcription': 'new_token'}
    new_token = Token.insert_before(token2.id, new_token_data)

    # Reload tokens from the database
    token1.refresh_from_db()
    token2.refresh_from_db()
    token3.refresh_from_db()

    # Check that the tokens were linked correctly
    assert token1.next == new_token
    assert new_token.previous == token1
    assert new_token.next == token2
    assert token2.previous == new_token
    assert token2.next == token3
    assert token3.previous == token2
    #print out the numbers
    print(token1.number)
    print(new_token.number)
    print(token2.number)
    print(token3.number)


@pytest.mark.django_db
def test_insert_after():
    # Create a text to associate tokens with
    text = TextFactory()

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2
    token2.previous = token1
    token2.next = token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()

    # Insert a new token after the last token (token3 in this case)
    new_token_data = {'transcription': 'new_token'}
    new_token = Token.insert_after(token3.id, new_token_data)  # Change to token3 which is the last

    # Reload tokens from the database to ensure all changes are reflected
    token1.refresh_from_db()
    token2.refresh_from_db()
    token3.refresh_from_db()
    new_token.refresh_from_db()  # Make sure to refresh the new_token as well

    # Assert conditions after insertion
    assert token3.next == new_token, "Token3's 'next' should be set to the new token"
    assert new_token.previous == token3, "New token's 'previous' should be token3"
    # Try to access new_token.next, and confirm it raises the expected exception since it should not exist
    try:
        next_of_new_token = new_token.next
        has_next = True  # If this line is reached, new_token.next exists which is not expected
    except Token.next.RelatedObjectDoesNotExist:
        has_next = False  # Catching the exception is the expected behavior

    assert not has_next, "New token's 'next' should be None since it's the last"
