from uuid import UUID
from django.test import TestCase

from mpcd.dict.models import (
    Category,
    Definition,
    Dictionary,
    Entry,
    LoanWord,
    Reference,
    Translation,
    Word,
)

class CategoryTestCase(TestCase):
    """ TEST BASIC USABILITY OF CATEGORY """
    def setUp(self):
        Category.objects.create(category='astr')

    def test_create_category(self):
        response = Category.objects.create(category='bot')
        self.assertIsInstance(response,Category)

    def test_get_category(self):
        response = Category.objects.get(category='astr')
        self.assertIsInstance(response,Category)
        self.assertEqual(response.category,'astr')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_category(self):
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(category='test_case')


class DefinitionTestCase(TestCase):
    """ TEST BASIC USABILITY OF DEFINITION"""
    def setUp(self):
        Definition.objects.create(definition='test_definition',language='eng')

    def test_get_definition(self):
        response = Definition.objects.get(definition='test_definition')
        self.assertIsInstance(response,Definition)
        self.assertEqual(response.definition,'test_definition')
        self.assertEqual(response.language,'eng')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_definiton(self):
        with self.assertRaises(Definition.DoesNotExist):
            Definition.objects.get(definition='test_case')


class DictionaryTestCase(TestCase):
    """ TEST BASIC USABILITY OF DICTIONARY"""
    def setUp(self):
        Dictionary.objects.create(name='test_dict',slug='eng')

    def test_get_dictionary(self):
        response = Dictionary.objects.get(name='test_dict')
        self.assertIsInstance(response,Dictionary)
        self.assertEqual(response.name,'test_dict')
        self.assertEqual(response.slug,'eng')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_dictionary(self):
        with self.assertRaises(Dictionary.DoesNotExist):
            Dictionary.objects.get(name='test_case')


class TranslationTestCase(TestCase):
    """ TEST BASIC USABILITY OF TRANSLATION """
    def setUp(self):
        Translation.objects.create(language='eng',meaning='test')

    def test_get_translation(self):
        response = Translation.objects.get(meaning='test')
        self.assertIsInstance(response,Translation)
        self.assertEqual(response.meaning,'test')
        self.assertEqual(response.language,'eng')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_translation(self):
        with self.assertRaises(Translation.DoesNotExist):
            Translation.objects.get(meaning='test_case')


class LoanWordTestCase(TestCase):
    """ TEST BASIC USABILITY OF LOANWORD"""
    def setUp(self):
        response = Translation.objects.create(language='eng',meaning='test')
        loanword = LoanWord.objects.create(word='test_loanword',language='eng')
        loanword.translations.set([response.id])

    def test_get_loanword(self):
        response = LoanWord.objects.get(word='test_loanword')
        self.assertIsInstance(response,LoanWord)
        self.assertEqual(response.word,'test_loanword')
        self.assertEqual(response.language,'eng')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_loanword(self):
        with self.assertRaises(LoanWord.DoesNotExist):
            LoanWord.objects.get(word='test_case')

class WordTestCase(TestCase):
    def setUp(self):
        Word.objects.create(word='test',language='eng')

    def test_get_word(self):
        response = Word.objects.get(word='test')
        self.assertIsInstance(response,Word)
        self.assertEqual(response.word,'test')
        self.assertEqual(response.language,'eng')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_word(self):
        with self.assertRaises(Word.DoesNotExist):
            Word.objects.get(word='test_case')

class ReferenceTestCase(TestCase):
    def setUp(self):
        Reference.objects.create(reference='test_ref',url='https://www.google.com')

    def test_get_reference(self):
        response = Reference.objects.get(reference='test_ref')
        self.assertIsInstance(response,Reference)
        self.assertEqual(response.reference,'test_ref')
        self.assertEqual(response.url,'https://www.google.com')
        self.assertIsInstance(response.id,UUID)

    def test_get_wrong_reference(self):
        with self.assertRaises(Reference.DoesNotExist):
            Reference.objects.get(reference='test_case')
