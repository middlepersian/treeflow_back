# Create your tests here.
from django.test import TestCase
from treeflow.corpus.models import Token, Section, SectionToken
from treeflow.search.logic import find_sections_with_tokens_logic
import asyncio
import logging

class FindSectionsWithTokensTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        logging.disable(logging.NOTSET)  # Re-enable logg
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

        section3 = Section.objects.create(type="sentence")
        SectionToken.objects.create(token=token4, section=section3)
        SectionToken.objects.create(token=token5, section=section3)
        SectionToken.objects.create(token=token1, section=section3)  # Reusing tokens in different sections

        # Create some sections
        section1 = Section.objects.create(type="sentence")
        section2 = Section.objects.create(type="sentence")
        section3 = Section.objects.create(type="sentence")
        
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
        


    def test_find_sections_with_two_tokens_in_sequence(self):
        # Define the search criteria
        criteria = [
            {"field": "transcription", "value": "apple"},
            {"field": "transcription", "value": "banana"}
        ]
        
        # Call the function
        result = find_sections_with_tokens_logic(criteria, "sentence", "sequence", False)
        
        # Assert the expected result
        self.assertEqual(len(result), 1)
        
        # Get the tokens from the first matching section
        tokens = result[0].tokens.all().order_by('number')
        
        self.assertEqual(tokens[0].transcription, "apple")
        self.assertEqual(tokens[1].transcription, "banana")
