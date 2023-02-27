from datetime import datetime
from django.test import TestCase
from django.db import models
from treeflow.corpus.documents.token import TokenDocument
from treeflow.corpus.models import Token
from treeflow.corpus.models import Section

'''
def test_token_document(self):


    # Create a new instance of the TokenDocument class
    token_doc = TokenDocument(
        id='1',
        number=1.0,
        number_in_sentence=1.0,
        root=True,
        word_token=True,
        visible=True,
        language='en',
        transcription='dffb fgb',
        transliteration='vdfvdfbvdrsbv',
        avestan='ertbrtbn',
        created_at=datetime.now()
    )

    # check that the document is not in the index
    self.assertEqual(TokenDocument.django.model, Token)
'''

class TokenDocumentTest(TestCase):
    def test_model_class_added(self):
        self.assertEqual(TokenDocument.django.model, Token)


    def test_get_queryset(self):
        qs = TokenDocument().get_queryset()
        self.assertIsInstance(qs, models.QuerySet)
        self.assertEqual(qs.model, Token)     


        