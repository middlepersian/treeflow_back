# Create your tests here.
from django.test import TestCase
from treeflow.corpus.models import Token, Section, SectionToken
from treeflow.search.logic import find_sections_with_tokens_logic
import asyncio
import logging

logger = logging.getLogger(__name__)

class FindSectionsWithTokensTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #logging.disable(logging.NOTSET)  # Re-enable logg
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
        
        # Create relationships between tokens and sections

        SectionToken.objects.create(token=token1, section=section1)
        SectionToken.objects.create(token=token2, section=section1)
        SectionToken.objects.create(token=token3, section=section1)
        SectionToken.objects.create(token=token4, section=section1)
        SectionToken.objects.create(token=token5, section=section1)
        SectionToken.objects.create(token=token6, section=section1)
        SectionToken.objects.create(token=token7, section=section1)

        SectionToken.objects.create(token=token3, section=section2)
        SectionToken.objects.create(token=token4, section=section2)
        SectionToken.objects.create(token=token5, section=section2)
        SectionToken.objects.create(token=token6, section=section2)
        SectionToken.objects.create(token=token7, section=section2)
        SectionToken.objects.create(token=token8, section=section2)

        SectionToken.objects.create(token=token4, section=section3)
        SectionToken.objects.create(token=token5, section=section3)
        SectionToken.objects.create(token=token6, section=section3)
        SectionToken.objects.create(token=token7, section=section3)
        SectionToken.objects.create(token=token8, section=section3)
        SectionToken.objects.create(token=token1, section=section3)  


        # Create a new section
        section5 = Section.objects.create(type="sentence")

        # Create relationships between tokens and the new section
        SectionToken.objects.create(token=token1, section=section5)  # apple
        SectionToken.objects.create(token=token2, section=section5)  # banana
        SectionToken.objects.create(token=token3, section=section5)  # cherry
        SectionToken.objects.create(token=token4, section=section5)  # date
        SectionToken.objects.create(token=token5, section=section5)  # elderberry
        SectionToken.objects.create(token=token6, section=section5)  # fig

        # Create a new section for distance test
        section_distance_test = Section.objects.create(type="sentence")

        # Create relationships between tokens and the new section
        SectionToken.objects.create(token=token1, section=section_distance_test)  # apple
        SectionToken.objects.create(token=token4, section=section_distance_test)  # date, 3 tokens away
        SectionToken.objects.create(token=token7, section=section_distance_test)  # grape, 2 tokens away


        


    def test_find_sections_with_two_tokens_in_sequence(self):
        # Define the search criteria
        criteria = [
            {"field": "transcription", "value": "apple"},
            {"field": "transcription", "value": "banana"}
        ]
        
        # Call the function
        result = find_sections_with_tokens_logic(criteria, "sentence", "sequence", False)
        
        # Assert the expected result
        self.assertEqual(len(result), 2)
        
        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')
        
        self.assertEqual(tokens[0].transcription, "apple")
        self.assertEqual(tokens[1].transcription, "banana")


    def test_find_sections_with_tokens_based_on_distance_without_enforcing_order(self):
        # Define the search criteria with min_previous_distance
        criteria = [
            {"field": "transcription", "value": "date"},
            {
                "field": "transcription",
                "value": "fig",
                "min_previous_distance": {"distance_from_previous": 2, "exact": True}
            }
        ]

        # Call the function with enforce_order set to False
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", False)

        # Assert the expected result
        self.assertEqual(len(result), 4)
        
        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that "date" is followed by "fig" (not necessarily immediately if order is not enforced)
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertIn("fig", [token.transcription for token in tokens[date_index+1:]])



    def test_find_adjacent_tokens_with_order(self):
        # Define the search criteria for adjacent tokens with order
        criteria = [
            {"field": "transcription", "value": "date"},
            {
                "field": "transcription",
                "value": "elderberry",
                "min_previous_distance": {"distance_from_previous": 0, "exact": True}
            }
        ]

        # Call the function with order enforced
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", True)

        # Assert the expected result: there should be sections that match the criteria
        self.assertGreater(len(result), 0)

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that "date" is immediately followed by "elderberry"
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertEqual(tokens[date_index + 1].transcription, "elderberry")


    def test_find_adjacent_tokens_without_order(self):
        # Define the search criteria for adjacent tokens without order
        criteria = [
            {"field": "transcription", "value": "date"},
            {
                "field": "transcription",
                "value": "elderberry",
                "min_previous_distance": {"distance_from_previous": 0, "exact": True}
            }
        ]

        # Call the function without order enforced
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", False)

        # Assert the expected result: there should be sections that match the criteria
        self.assertGreater(len(result), 0)

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that "date" and "elderberry" are adjacent, without considering the order
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        elderberry_index = next((i for i, token in enumerate(tokens) if token.transcription == "elderberry"), None)

        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertIsNotNone(elderberry_index, "Elderberry token not found in the result.")
        self.assertTrue(abs(date_index - elderberry_index) == 1, "Tokens are not adjacent.")


    def test_find_three_tokens_distance_with_order(self):
        # Define the search criteria for a sequence of three tokens with order
        criteria = [
            {"field": "transcription", "value": "date"},
            {"field": "transcription", "value": "elderberry", "min_previous_distance": {"distance_from_previous": 0, "exact": True}},
            {"field": "transcription", "value": "fig", "min_previous_distance": {"distance_from_previous": 0, "exact": True}}
        ]

        # Call the function with order enforced
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", True)

        # Assert the expected result: there should be sections that match the criteria
        self.assertGreater(len(result), 0)

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that the tokens appear in sequence
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        elderberry_index = next((i for i, token in enumerate(tokens) if token.transcription == "elderberry"), None)
        fig_index = next((i for i, token in enumerate(tokens) if token.transcription == "fig"), None)

        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertIsNotNone(elderberry_index, "Elderberry token not found in the result.")
        self.assertIsNotNone(fig_index, "Fig token not found in the result.")
        self.assertTrue(date_index < elderberry_index < fig_index, "Tokens are not in sequence.")


    def test_find_three_tokens_distance_without_order(self):
        # Define the search criteria for a sequence of three tokens without order
        criteria = [
            {"field": "transcription", "value": "date"},
            {"field": "transcription", "value": "fig"},
            {"field": "transcription", "value": "elderberry"}
        ]

        # Call the function without order enforced
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", False)

        # Assert the expected result: there should be sections that match the criteria
        self.assertGreater(len(result), 0)

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that the tokens appear in the result, regardless of order
        self.assertTrue(any(token.transcription == "date" for token in tokens))
        self.assertTrue(any(token.transcription == "elderberry" for token in tokens))
        self.assertTrue(any(token.transcription == "fig" for token in tokens))


    def test_find_three_tokens_with_specified_distances(self):
        # Define the search criteria for a sequence of three tokens with specific distances
        criteria = [
            {"field": "transcription", "value": "apple"},
            {"field": "transcription", "value": "date", "min_previous_distance": {"distance_from_previous": 3, "exact": True}},
            {"field": "transcription", "value": "fig", "min_previous_distance": {"distance_from_previous": 2, "exact": True}}
        ]

        # Call the function
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", False)

        # Assert the expected result: there should be sections that match the criteria
        self.assertGreater(len(result), 1)

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that the tokens appear in the result
        self.assertTrue(any(token.transcription == "apple" for token in tokens))
        self.assertTrue(any(token.transcription == "date" for token in tokens))
        self.assertTrue(any(token.transcription == "fig" for token in tokens))

        # Assert the distances between the tokens
        apple_index = next((i for i, token in enumerate(tokens) if token.transcription == "apple"), None)
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        fig_index = next((i for i, token in enumerate(tokens) if token.transcription == "fig"), None)

        self.assertIsNotNone(apple_index, "Apple token not found in the result.")
        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertIsNotNone(fig_index, "Fig token not found in the result.")
        self.assertTrue(date_index - apple_index == 3, "Distance between apple and date is not correct.")
        self.assertTrue(fig_index - date_index == 2, "Distance between date and fig is not correct.")

    def test_find_sections_with_tokens_based_on_multiple_distances(self):
        # Define the search criteria with min_previous_distance for multiple distances
        criteria = [
            {"field": "transcription", "value": "apple"},
            {
                "field": "transcription",
                "value": "date",
                "min_previous_distance": {"distance_from_previous": 3, "exact": True}
            },
            {
                "field": "transcription",
                "value": "grape",
                "min_previous_distance": {"distance_from_previous": 2, "exact": True}
            }
        ]

        # Call the function with enforce_order set to False
        result = find_sections_with_tokens_logic(criteria, "sentence", "distance", False)

        logger.debug("Result:")

        for sec in result:
            tokens = sec.tokens.all().order_by('number')
            logger.info([token.transcription for token in tokens])


        # Assert the expected result
        self.assertEqual(len(result), 1, f"Expected 1 section, but got {len(result)}. Sections: {[sec.id for sec in result]}")

        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')

        # Assert that the tokens appear in the expected order and distance
        apple_index = next((i for i, token in enumerate(tokens) if token.transcription == "apple"), None)
        date_index = next((i for i, token in enumerate(tokens) if token.transcription == "date"), None)
        grape_index = next((i for i, token in enumerate(tokens) if token.transcription == "grape"), None)

        self.assertIsNotNone(apple_index, "Apple token not found in the result.")
        self.assertIsNotNone(date_index, "Date token not found in the result.")
        self.assertIsNotNone(grape_index, "Grape token not found in the result.")
        self.assertTrue(date_index - apple_index == 2, "Distance between apple and date is not correct.")
        self.assertTrue(grape_index - date_index == 1, "Distance between date and grape is not 2.")
