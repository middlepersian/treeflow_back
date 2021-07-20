import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from physical import Line


class TokenSemantics(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    meaning = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class MorphologicalAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)

    class PosTag(models.TextChoices):
        ADJ = 'ADJ', 'Adjective'
        ADP = 'ADP', 'Adposition'
        ADV = "ADV", "Adverb"
        AUX = "AUX", "auxiliary"   
        CCONJ =  "CCONJ", "Coordinating conjunction"
        DET = "DET", "Determiner"
        INTJ = "INTJ", "Interjection"
        NOUN = "NOUN", "Noun"
        NUM =   "NUM", "Numeral"
        PART =  "PART", "Particle"
        PRON = "PRON", "Pronoun"    
        PROPN = "PROPN", "Proper noun"
        PUNCT = "PUNCT", "Punctuation"
        SCONJO =  "SCONJO", "Subordinating conjunction"
        SYM = "SYM", "Symbol"
        VERB = "VERB", "Verb"
        X = "X", "Other"

    pos_tag = models.CharField(max_length=6, choices=PosTag.choices)


class Token(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    line_id = models.ForeignKey(Line, on_delete=models.SET_NULL)
    tkn = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    lemma = models.ForeignKey()

    
    morph_annotations = models.ForeignKey(MorphologicalAnnotation, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True)

    avestan = models.CharField(max_length=255, blank=True)
