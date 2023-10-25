# Create your tests here.
from django.test import TestCase
from treeflow.corpus.models import Token, Section, SectionToken
from treeflow.corpus.types.token import TokenSearchInput, DistanceFromPreviousToken
from treeflow.search.logic import search_tokens, search_tokens_by_position
import asyncio
import logging


logger = logging.getLogger(__name__)


class TokenSearchTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create some tokens based on their numbers
        cls.token1 = Token.objects.create(transcription="apple", number=1)
        cls.token2 = Token.objects.create(transcription="banana", number=2)
        cls.token3 = Token.objects.create(transcription="cherry", number=3)
        cls.token4 = Token.objects.create(transcription="date", number=4)
        cls.token5 = Token.objects.create(transcription="elderberry", number=5)
        cls.token6 = Token.objects.create(transcription="fig", number=6)
        cls.token7 = Token.objects.create(transcription="grape", number=7)
        cls.token8 = Token.objects.create(transcription="honeydew", number=8)
        cls.token9 = Token.objects.create(transcription="imbe", number=9)

        # Create some sections
        cls.section1 = Section.objects.create(type="sentence")
        cls.section2 = Section.objects.create(type="sentence")
        cls.section3 = Section.objects.create(type="sentence")
        cls.section4 = Section.objects.create(type="sentence")
        cls.section5 = Section.objects.create(type="sentence")
        cls.section6 = Section.objects.create(type="sentence")
        cls.section7 = Section.objects.create(type="sentence")

        # cls.section1: apple(1), banana(2), cherry(3), date(4), elderberry(5), grape(7), honeydew(8), imbe(9)
        for token in sorted([cls.token1, cls.token2, cls.token3, cls.token4, cls.token5, cls.token7, cls.token8, cls.token9], key=lambda x: x.number):
            SectionToken.objects.create(token=token, section=cls.section1)

        # cls.section2: apple(1), banana(2), cherry(3), date(4), fig(6), grape(7), honeydew(8), imbe(9)
        for token in sorted([cls.token1, cls.token2, cls.token3, cls.token4, cls.token6, cls.token7, cls.token8, cls.token9], key=lambda x: x.number):
            SectionToken.objects.create(token=token, section=cls.section2)

        # cls.section3: apple(1), banana(2), cherry(3), date(4), elderberry(5), fig(6), grape(7), honeydew(8), imbe(9)
        for token in sorted([cls.token1, cls.token2, cls.token3, cls.token4, cls.token5, cls.token6, cls.token7, cls.token8, cls.token9], key=lambda x: x.number, reverse=True):
            SectionToken.objects.create(token=token, section=cls.section3)

        # cls.section4: apple(1), banana(2), elderberry(5), grape(7), honeydew(8)
        for token in sorted([cls.token1, cls.token2, cls.token5, cls.token7, cls.token8], key=lambda x: x.number):
            SectionToken.objects.create(token=token, section=cls.section4)

        # cls.section5: apple(1), banana(2), cherry(3), date(4), fig(6), grape(7), honeydew(8), imbe(9)
        for token in sorted([cls.token9, cls.token2, cls.token3, cls.token8, cls.token1, cls.token6, cls.token4, cls.token7], key=lambda x: x.number):
            SectionToken.objects.create(token=token, section=cls.section5)

        # cls.section6: apple(1), fig(6), grape(7)
        for token in sorted([cls.token1, cls.token6, cls.token7], key=lambda x: x.number):
            SectionToken.objects.create(token=token, section=cls.section6)

    def test_search_tokens(self):
        # Test with a single criteria
        criteria_list = [
            TokenSearchInput(field="transcription", value="apple", query_type="icontains", distance_from_previous=None)
        ]
        highlighted_sections = search_tokens(criteria_list, "sentence")
        # apple is present in section1, section2, section3, section4, section5, and section6
        self.assertEqual(len(highlighted_sections), 6)
        for section_data in highlighted_sections:
            self.assertTrue(any(token.transcription.lower() == "apple" for token in section_data['highlighted_tokens']))

        # Test with multiple criteria
        criteria_list = [
            TokenSearchInput(field="transcription", value="apple", query_type="icontains", distance_from_previous=None),
            TokenSearchInput(field="transcription", value="banana", query_type="icontains", distance_from_previous=None)
        ]
        highlighted_sections = search_tokens(criteria_list, "sentence")
        # Both apple and banana are present in section1, section2, section3, section4, and section5
        self.assertEqual(len(highlighted_sections), 5)
        for section_data in highlighted_sections:
            self.assertTrue(any(token.transcription.lower() == "apple" for token in section_data['highlighted_tokens']))
            self.assertTrue(any(token.transcription.lower() ==
                            "banana" for token in section_data['highlighted_tokens']))

        # Test with non-existing token
        criteria_list = [
            TokenSearchInput(field="transcription", value="non_existent",
                             query_type="icontains", distance_from_previous=None)
        ]
        highlighted_sections = search_tokens(criteria_list, "sentence")
        self.assertEqual(len(highlighted_sections), 0)  # No sections should match this criteria

    def test_search_tokens_by_position(self):

        # Subtest 1: Find sections with 'apple' followed by 'banana' with a distance of 1
        with self.subTest("Test with two tokens: apple followed by banana with a distance of 1"):
            criteria_list = [
                TokenSearchInput(value="apple", distance_from_previous=None),
                TokenSearchInput(value="banana", distance_from_previous=DistanceFromPreviousToken(
                    distance=1, exact=True))
            ]
            highlighted_sections = search_tokens_by_position(criteria_list, "sentence")
            expected_sections = {self.section1, self.section2, self.section3, self.section4, self.section5}
            self.assertSetEqual({s['section'] for s in highlighted_sections}, expected_sections)

        # Subtest 2: Find sections with 'apple' followed by 'banana' with a distance of 1, followed by 'cherry' with a distance of 1
        with self.subTest("Test with three tokens: apple, banana, cherry with specific distances"):
            criteria_list = [
                TokenSearchInput(value="apple", distance_from_previous=None),
                TokenSearchInput(value="banana", distance_from_previous=DistanceFromPreviousToken(
                    distance=1, exact=True)),
                TokenSearchInput(value="cherry", distance_from_previous=DistanceFromPreviousToken(
                    distance=1, exact=True))
            ]
            highlighted_sections = search_tokens_by_position(criteria_list, "sentence")
            expected_sections = {self.section1, self.section2, self.section3,  self.section5}
            self.assertSetEqual({s['section'] for s in highlighted_sections}, expected_sections)

        # Subtest 3: Find sections with 'apple' followed by 'banana' with a distance of 1, followed by 'cherry' with a distance of 1, followed by 'date' with a distance of 1
        with self.subTest("Test with four tokens: apple, banana, cherry, date with specific distances"):
            criteria_list = [
                TokenSearchInput(value="apple", distance_from_previous=None),
                TokenSearchInput(value="banana", distance_from_previous=DistanceFromPreviousToken(
                    distance=1, exact=True)),
                TokenSearchInput(value="cherry", distance_from_previous=DistanceFromPreviousToken(
                    distance=1, exact=True)),
                TokenSearchInput(value="date", distance_from_previous=DistanceFromPreviousToken(distance=1, exact=True))
            ]
            highlighted_sections = search_tokens_by_position(criteria_list, "sentence")
            expected_sections = {self.section1, self.section2, self.section3,  self.section5}
            self.assertSetEqual({s['section'] for s in highlighted_sections}, expected_sections)
