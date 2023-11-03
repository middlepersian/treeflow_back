# Create your tests here.
from django.test import TestCase
from django.db.models import Q
from treeflow.corpus.models import Token, Section, SectionToken, POS, Feature
from treeflow.dict.models import Lemma
from treeflow.corpus.types.token import TokenSearchInput, Distance, FeatureSelectionInput, POSSelectionInput
from treeflow.search.logic import retrieve_initial_anchors, identify_candidate_sections
import asyncio
import logging


logger = logging.getLogger(__name__)


class TokenSearchTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create tokens with mixed order of transcriptions and numbers
        cls.token_apple = Token.objects.create(transcription="apple", number=1)
        cls.token_pear = Token.objects.create(transcription="pear", number=2)
        cls.token_cherry = Token.objects.create(transcription="cherry", number=4)
        cls.token_grape = Token.objects.create(transcription="grape", number=5)
        cls.token_banana = Token.objects.create(transcription="banana", number=7)
        cls.token_mango = Token.objects.create(transcription="mango", number=8)
        cls.token_pineapple = Token.objects.create(transcription="pineapple", number=11)
        cls.token_fruit = Token.objects.create(transcription="fruit", number=10)
        cls.token_sweet = Token.objects.create(transcription="sweet", number=14)
        cls.token_delicious = Token.objects.create(transcription="delicious", number=13)
        cls.token_fresh = Token.objects.create(transcription="fresh", number=16)
        cls.token_ripe = Token.objects.create(transcription="ripe", number=17)
        cls.token_juicy = Token.objects.create(transcription="juicy", number=19)
        cls.token_tart = Token.objects.create(transcription="tart", number=20)

        # Create some sections with these tokens
        cls.section1 = Section.objects.create(type="sentence")
        cls.section2 = Section.objects.create(type="sentence")
        cls.section3 = Section.objects.create(type="sentence")
        cls.section4 = Section.objects.create(type="sentence")
        cls.section5 = Section.objects.create(type="sentence")
        cls.section6 = Section.objects.create(type="sentence")
        cls.section7 = Section.objects.create(type="sentence")

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

        # cls.section6: pear(2), grape(5), mango(8), pineapple(11), sweet(14)
        for token in [cls.token_pear, cls.token_grape, cls.token_mango, cls.token_pineapple, cls.token_sweet]:
            SectionToken.objects.create(token=token, section=cls.section6)

        # cls.section7: ripe(17), tart(20), pear(2), mango(8)
        for token in [cls.token_ripe, cls.token_tart, cls.token_pear, cls.token_mango]:
            SectionToken.objects.create(token=token, section=cls.section7)


        # Additional lemmas
        cls.lemma_pear = Lemma.objects.create(word="pear", language="en")
        cls.lemma_grape = Lemma.objects.create(word="grape", language="en")
        cls.lemma_mango = Lemma.objects.create(word="mango", language="en")
        cls.lemma_pineapple = Lemma.objects.create(word="pineapple", language="en")
        cls.lemma_ripe = Lemma.objects.create(word="ripe", language="en")
        cls.lemma_tart = Lemma.objects.create(word="tart", language="en")

        # Associate tokens with these lemmas
        cls.token_pear.lemmas.add(cls.lemma_pear)
        cls.token_grape.lemmas.add(cls.lemma_grape)
        cls.token_mango.lemmas.add(cls.lemma_mango)
        cls.token_pineapple.lemmas.add(cls.lemma_pineapple)
        cls.token_ripe.lemmas.add(cls.lemma_ripe)
        cls.token_tart.lemmas.add(cls.lemma_tart)

        # Create some POS entries
        cls.pos_noun_apple = POS.objects.create(token=cls.token_apple, pos="noun", type="upos")
        cls.pos_noun_banana = POS.objects.create(token=cls.token_banana, pos="noun", type="upos")
        cls.pos_adjective_delicious = POS.objects.create(token=cls.token_delicious, pos="adjective", type="upos")
        cls.pos_verb_eat = POS.objects.create(token=cls.token_mango, pos="verb", type="upos")
        cls.pos_adjective_ripe = POS.objects.create(token=cls.token_ripe, pos="adjective", type="upos")

        # Create some features for tokens
        cls.feature_singular_apple = Feature.objects.create(
            token=cls.token_apple, pos=cls.pos_noun_apple, feature="number", feature_value="singular")
        cls.feature_plural_banana = Feature.objects.create(
            token=cls.token_banana, pos=cls.pos_noun_banana, feature="number", feature_value="plural")
        cls.feature_taste_delicious = Feature.objects.create(
            token=cls.token_delicious, pos=cls.pos_adjective_delicious, feature="taste", feature_value="sweet")
        cls.feature_singular_pear = Feature.objects.create(
            token=cls.token_pear, pos=cls.pos_verb_eat, feature="number", feature_value="singular")
        cls.feature_taste_ripe = Feature.objects.create(
            token=cls.token_ripe, pos=cls.pos_adjective_ripe, feature="taste", feature_value="sweet")

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

    def test_retrieve_initial_anchors_exact(self):
        # This test ensures that the exact match query returns only the exact matches
        criterion = TokenSearchInput(field='transcription', value='apple', query_type='exact')
        result = retrieve_initial_anchors(criterion)
        self.assertIn(self.token_apple, result)
        self.assertEqual(len(result), 1)  # Only one exact match for 'apple'

    def test_retrieve_initial_anchors_contains(self):
        # This test checks that the contains query returns all tokens that contain the string
        criterion = TokenSearchInput(field='transcription', value='ap', query_type='contains')
        result = retrieve_initial_anchors(criterion)
        self.assertIn(self.token_apple, result)  # 'apple' contains 'ap'
        self.assertIn(self.token_grape, result)  # 'grape' contains 'ap'
        self.assertIn(self.token_pineapple, result)  # 'pineapple' contains 'ap'
        # Assert that the number of returned tokens matches the expected
        self.assertEqual(len(result), 3)

    def test_retrieve_initial_anchors_unsupported_query_type(self):
        # This test checks that an unsupported query type returns an empty list
        criterion = TokenSearchInput(field='transcription', value='apple', query_type='unsupported')
        result = retrieve_initial_anchors(criterion)
        self.assertEqual(result, [])  # Expecting an empty list for unsupported query types


    def test_identify_candidate_sections_with_anchors(self):
        # Test with a list of tokens that should belong to multiple sections
        anchors = [self.token_apple, self.token_banana]
        expected_section_ids = {
            self.section1.id, self.section2.id, self.section3.id, 
            self.section4.id, self.section5.id  # These are the sections we expect
        }
        
        result_sections = identify_candidate_sections(anchors)
        result_section_ids = {section.id for section in result_sections}
        self.assertEqual(result_section_ids, expected_section_ids)

    def test_identify_candidate_sections_no_anchors(self):
        # Test with an empty list of tokens
        result_sections = identify_candidate_sections([])
        self.assertEqual(result_sections, [])