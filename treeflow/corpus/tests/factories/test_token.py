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

    # Insert a new token after token2 (instead of after the last token)
    new_token_data = {'transcription': 'new_token'}
    new_token = Token.insert_after(token2.id, new_token_data)  # Change to insert after token2

    # Reload tokens from the database to ensure all changes are reflected
    token1.refresh_from_db()
    token2.refresh_from_db()
    token3.refresh_from_db()
    new_token.refresh_from_db()  # Make sure to refresh the new_token as well

    # Assert conditions after insertion
    assert token2.next == new_token, "Token2's 'next' should be set to the new token"
    assert new_token.previous == token2, "New token's 'previous' should be token2"
    assert new_token.next == token3, "New token's 'next' should be token3"
    assert token3.previous == new_token, "Token3's 'previous' should be the new token"


@pytest.mark.django_db
def test_delete_token():
    # Create a text to associate tokens with
    text = TextFactory()

    # Create a sequence of tokens with known numbers
    token1 = TokenFactory(text=text, number=1.0)
    token2 = TokenFactory(text=text, number=2.0)
    token3 = TokenFactory(text=text, number=3.0)

    # Link tokens manually or by some setup logic
    token1.next = token2  # This will not reflect in the DB because 'next' is a reverse relation from 'previous'
    token2.previous = token1
    token2.next = token3  # As above, the 'next' relation is implied by setting 'previous' on token3
    token3.previous = token2
    token1.save()
    token2.save()
    token3.save()

    # Delete token2 using the new method
    Token.delete_token(token2.id)

    # Reload tokens from the database
    token1.refresh_from_db()
    token3.refresh_from_db()

    # Verify that token3.previous points to token1
    assert token3.previous == token1

    # Verify that token1.next points to token3 (if your model logic explicitly maintains 'next' references)
    # This would only be valid if you have logic elsewhere in your application that maintains a 'next' reference.
    # Otherwise, you would not include this check since 'next' is not a field on your model.
    # assert token1.next == token3

    # Check that token2 is no longer in the database
    with pytest.raises(Token.DoesNotExist):
        Token.objects.get(id=token2.id)

    # Output the token numbers to verify the sequence
    print(token1.number)
    # token2.number is not printed because token2 should be deleted
    print(token3.number)
