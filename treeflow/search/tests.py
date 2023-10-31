# Create your tests here.
from django.test import TestCase
from django.db.models import Q
from treeflow.corpus.models import Token, Section, SectionToken, POS, Feature
from treeflow.dict.models import Lemma
from treeflow.corpus.types.token import TokenSearchInput, Distance, FeatureSelectionInput, POSSelectionInput
from treeflow.search.logic import build_query_for_criteria, search_tokens_in_sequence, get_sections_for_matched_tokens
import asyncio
import logging


logger = logging.getLogger(__name__)


class TokenSearchTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create tokens with mixed order of transcriptions and numbers
        cls.token_apple = Token.objects.create(transcription="apple", number=1)
        cls.token_cherry = Token.objects.create(transcription="cherry", number=4)
        cls.token_banana = Token.objects.create(transcription="banana", number=7)
        cls.token_fruit = Token.objects.create(transcription="fruit", number=10)
        cls.token_delicious = Token.objects.create(transcription="delicious", number=13)
        cls.token_fresh = Token.objects.create(transcription="fresh", number=16)
        cls.token_juicy = Token.objects.create(transcription="juicy", number=19)

        # Create some sections with these tokens
        cls.section1 = Section.objects.create(type="sentence")
        cls.section2 = Section.objects.create(type="sentence")
        cls.section3 = Section.objects.create(type="sentence")
        cls.section4 = Section.objects.create(type="sentence")
        cls.section5 = Section.objects.create(type="sentence")

        # cls.section1: apple(1), cherry(4), banana(7), fruit(10), delicious(13)
        for token in [cls.token_apple, cls.token_cherry, cls.token_banana, cls.token_fruit, cls.token_delicious]:
            SectionToken.objects.create(token=token, section=cls.section1)

        # cls.section2: apple(1), banana(7), cherry(4), fruit(10), fresh(16), juicy(19)
        for token in [cls.token_apple, cls.token_banana, cls.token_cherry, cls.token_fruit, cls.token_fresh, cls.token_juicy]:
            SectionToken.objects.create(token=token, section=cls.section2)

        # cls.section3: cherry(4), apple(1), banana(7), fruit(10), juicy(19)
        for token in [cls.token_cherry, cls.token_apple, cls.token_banana, cls.token_fruit, cls.token_juicy]:
            SectionToken.objects.create(token=token, section=cls.section3)

        # cls.section4: banana(7), apple(1), cherry(4), juicy(19), delicious(13)
        for token in [cls.token_banana, cls.token_apple, cls.token_cherry, cls.token_juicy, cls.token_delicious]:
            SectionToken.objects.create(token=token, section=cls.section4)

        # cls.section5: delicious(13), fruit(10), juicy(19), fresh(16), apple(1), cherry(4), banana(7)
        for token in [cls.token_delicious, cls.token_fruit, cls.token_juicy, cls.token_fresh, cls.token_apple, cls.token_cherry, cls.token_banana]:
            SectionToken.objects.create(token=token, section=cls.section5)

        # Create some POS entries
        cls.pos_noun_apple = POS.objects.create(token=cls.token_apple, pos="noun", type="upos")
        cls.pos_noun_banana = POS.objects.create(token=cls.token_banana, pos="noun", type="upos")
        cls.pos_adjective_delicious = POS.objects.create(token=cls.token_delicious, pos="adjective", type="upos")

        # Create some features for tokens
        cls.feature_singular_apple = Feature.objects.create(
            token=cls.token_apple, pos=cls.pos_noun_apple, feature="number", feature_value="singular")
        cls.feature_plural_banana = Feature.objects.create(
            token=cls.token_banana, pos=cls.pos_noun_banana, feature="number", feature_value="plural")
        cls.feature_taste_delicious = Feature.objects.create(
            token=cls.token_delicious, pos=cls.pos_adjective_delicious, feature="taste", feature_value="sweet")

        # Create some lemmas
        cls.lemma_apple = Lemma.objects.create(word="apple", language="en")
        cls.lemma_banana = Lemma.objects.create(word="banana", language="en")
        cls.lemma_cherry = Lemma.objects.create(word="cherry", language="en")
        cls.lemma_delicious = Lemma.objects.create(word="delicious", language="en")

        # Associate tokens with these lemmas
        cls.token_apple.lemmas.add(cls.lemma_apple)
        cls.token_banana.lemmas.add(cls.lemma_banana)
        cls.token_cherry.lemmas.add(cls.lemma_cherry)
        cls.token_delicious.lemmas.add(cls.lemma_delicious)
    


    def test_construct_token_query_and_matching_sections(self):
        criteria1 = TokenSearchInput(query_type='exact', value='apple', field='transcription')
        criteria2 = TokenSearchInput(query_type='iexact', value='cherry', field='transcription', distance=Distance(distance=3, exact=False, type='after'))
        criteria3 = TokenSearchInput(query_type='exact', value='banana', field='transcription', distance=Distance(distance=3, exact=False, type='after'))

        # Test the `search_tokens_in_sequence` function using the constructed query.
        matched_sequences = search_tokens_in_sequence([criteria1, criteria2, criteria3])

        # Check that a sequence was found
        self.assertEqual(len(matched_sequences), 1)
        
        # Now get the first sequence from the list of sequences
        matching_tokens = matched_sequences[0]

        # Check that the correct tokens were returned based on the criteria.
        self.assertEqual(len(matching_tokens), 3)
        self.assertEqual(matching_tokens[0].transcription, "apple")
        self.assertEqual(matching_tokens[1].transcription, "cherry")
        self.assertEqual(matching_tokens[2].transcription, "banana")
        # Test the `get_sections_for_matched_tokens` function using the same criteria.
        matching_sections = get_sections_for_matched_tokens([criteria1, criteria2, criteria3])

        # Check that sections were returned.
        self.assertTrue(len(matching_sections) > 0)

        # log the length of the matching sections
        logger.debug(f"Found {len(matching_sections)} matching sections.")


        # Here, you might want to further validate the returned sections based on your data setup.
        # For example, you could check if the sections actually contain the tokens.
        for token in matching_tokens:
            token_in_section = any(section for section in matching_sections if token in section.tokens.all())
            self.assertTrue(token_in_section)
