import uuid as uuid_lib
from django.db import models


class PosCh(models.TextChoices):
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
    SCONJO = "SCONJO", "SCONJO"
    SYM = "SYM", "SYM"
    VERB = "VERB", "VERB"
    X = "X", "X"


class Pos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    pos = models.CharField(max_length=6, choices=PosCh.choices, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_pos",
                check=models.Q(pos__in=PosCh.values),
            )]

    def __str__(self):
        return '{}'.format(self.pos)
