# Create your tests here.
from django.test import TestCase
from treeflow.corpus.models import Token, Section, SectionToken
from treeflow.search.logic import get_sections_by_single_token_criteria, get_sections_by_multiple_token_criteria
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
        section6 = Section.objects.create(type="sentence")

        # Create relationships between tokens and sections

        # Add tokens to section1 in their original order
        # apple, banana, cherry, date, elderberry, grape, honeydew, imbe
        for token in [token1, token2, token3, token4, token5, token7, token8, token9]:
            SectionToken.objects.create(token=token, section=section1)

        # Add tokens to section2 in a different order (e.g., every second token followed by the remaining tokens)
        # apple, cherry, grape, imbe, banana, date, fig, honeydew
        for token in [token1, token3, token7, token9, token2, token4, token6, token8]:
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
        # imbe, banana, cherry, honeydew, apple, fig, date, grape
        for token in [token9, token2, token3, token8, token1, token6, token4, token7]:
            SectionToken.objects.create(token=token, section=section5)

        # add only three tokens to section6
        # apple, fig and grape
        for token in [token1, token6, token7]:
            SectionToken.objects.create(token=token, section=section6)

    def test_get_sections_with_criteria(self):
        # Test single criteria
        criteria = {
            "tokens__transcription": {"value": "apple", "method": "icontains"}
        }

        sections = get_sections_by_single_token_criteria(criteria, "sentence")
        # apple is present in section1, section2, section3, section4, section5 and section6
        self.assertEqual(len(sections), 6)

        criteria = {
            "tokens__transcription": {"value": "date", "method": "icontains"}
        }

        sections = get_sections_by_single_token_criteria(criteria, "sentence")
        self.assertEqual(len(sections), 4)  # date is present in section1, section2, section3, section5

        criteria = {
            "tokens__transcription": {"value": "non_existen", "method": "icontains"}
        }

        sections = get_sections_by_single_token_criteria(criteria, "sentence")
        self.assertEqual(len(sections), 0)  # No sections should match this criteria

    def test_get_sections_with_tokens(self):
        # Define section criteria (in this case, just the type of section)
        section_criteria = {
            "type": "sentence"
        }

        # Search for sections containing tokens with transcription "apple" AND "banana"
        token_criteria_list = [
            {"transcription": {"value": "apple", "method": "icontains"}},
            {"transcription": {"value": "banana", "method": "icontains"}}
        ]
        sections = get_sections_by_multiple_token_criteria(section_criteria, token_criteria_list)
        self.assertEqual(len(sections), 5)

        # Search for sections containing tokens with transcription "elderberry" AND "fig"
        token_criteria_list = [
            {"transcription": {"value": "elderberry", "method": "icontains"}},
            {"transcription": {"value": "fig", "method": "icontains"}}
        ]
        sections = get_sections_by_multiple_token_criteria(section_criteria, token_criteria_list)
        self.assertEqual(len(sections), 1)
