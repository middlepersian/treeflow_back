# Create your tests here.
from django.test import TestCase
from treeflow.corpus.models import Token, Section, SectionToken
from treeflow.search.logic import find_sections_with_ordered_tokens, get_sections_with_token, get_sections_with_token_position
import asyncio
import logging

logger = logging.getLogger(__name__)


class TokenSearchTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # logging.disable(logging.NOTSET)  # Re-enable logg
        # Create some tokens
        token1 = Token.objects.create(transcription="apple", number=1)
        token2 = Token.objects.create(transcription="banana", number=2)
        token3 = Token.objects.create(transcription="cherry", number=3)
        token4 = Token.objects.create(transcription="date", number=4)
        token5 = Token.objects.create(transcription="elderberry", number=5)
        token6 = Token.objects.create(transcription="fig", number=6)
        token7 = Token.objects.create(transcription="grape", number=7)
        token8 = Token.objects.create(transcription="honeydew", number=8)
        token9 = Token.objects.create(transcription="imbe", number=9)

        # Create some sections
        section1 = Section.objects.create(type="sentence")
        section2 = Section.objects.create(type="sentence")
        section3 = Section.objects.create(type="sentence")
        section4 = Section.objects.create(type="sentence")
        section5 = Section.objects.create(type="sentence")

        # Create relationships between tokens and sections

        # Add tokens to section1 in their original order
        # apple, banana, cherry, date, elderberry, fig, grape, honeydew, imbe
        for token in [token1, token2, token3, token4, token5, token6, token7, token8, token9]:
            SectionToken.objects.create(token=token, section=section1)

        # Add tokens to section2 in a different order (e.g., every second token followed by the remaining tokens)
        # apple, cherry, elderberry, grape, imbe, banana, date, fig, honeydew
        for token in [token1, token3, token5, token7, token9, token2, token4, token6, token8]:
            SectionToken.objects.create(token=token, section=section2)

        # Add tokens to section3 in a different order (e.g., reversed)
        # imbe, honeydew, grape, fig, elderberry, date, cherry, banana, apple
        for token in reversed([token1, token2, token3, token4, token5, token6, token7, token8, token9]):
            SectionToken.objects.create(token=token, section=section3)

        # Add tokens to section4 in their original order but skip some
        # apple, banana, elderberry, grape, honeydew
        for token in [token1, token2, token5, token7, token8]:
            SectionToken.objects.create(token=token, section=section4)

        # Add tokens to section5 in some custom order
        # imbe, banana, cherry, honeydew, elderberry, apple, fig, date, grape
        for token in [token9, token2, token3, token8, token5, token1, token6, token4, token7]:
            SectionToken.objects.create(token=token, section=section5)


    def test_find_sections_with_ordered_tokens(self):
        criteria = [
            {"field": "transcription", "value": "apple"},
            {"field": "transcription", "value": "banana"},
            {"field": "transcription", "value": "cherry"},
            {"field": "transcription", "value": "date"}
        ]

        # Call the search function
        result = find_sections_with_ordered_tokens(criteria, "sentence", enforce_order=True)

        # Assert that only the section with ordered tokens is returned
        self.assertEqual(len(result), 1)

    def test_get_sections_with_token(self):
        sections = get_sections_with_token("fig", "sentence")
        self.assertEqual(len(sections), 4)


"""     def test_search_three_tokens_without_order(self):
        # Define the search criteria
        criteria = [
            {"field": "transcription", "value": "apple"},
            {"field": "transcription", "value": "banana"},
            {"field": "transcription", "value": "cherry"}
        ]

        # Call the search function
        result = find_sections_with_all_tokens(criteria, "sentence")
        # Assert that the returned sections contain the correct tokens
        self.assertEqual(len(result), 4)  # Since four sections have all three tokens

        for section in result:
            tokens = set(token.transcription for token in section.tokens.all())
            self.assertTrue("apple" in tokens)
            self.assertTrue("banana" in tokens)
            self.assertTrue("cherry" in tokens) """

