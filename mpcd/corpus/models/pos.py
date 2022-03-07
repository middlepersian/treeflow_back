import uuid as uuid_lib
from django.db import models


class POSChoices(models.TextChoices):
    ADJ = 'ADJ', 'ADJ'
    ADP = 'ADP', 'ADP'
    ADV = "ADV", "ADV"
    AUX = "AUX", "AUX"
    CCONJ = "CCONJ", "CCONJ"
    DET = "DET", "DET"
    INTJ = "INTJ", "INTJ"
    NOUN = "NOUN", "NOUN"
    NUM = "NUM", "NUM"
    PART = "PART", "PART"
    PRON = "PRON", "PRON"
    PROPN = "PROPN", "PROPN"
    PUNCT = "PUNCT", "PUNCT"
    SCONJ = "SCONJ", "SCONJ"
    SYM = "SYM", "SYM"
    VERB = "VERB", "VERB"
    X = "X", "X"

