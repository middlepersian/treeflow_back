import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

from .meaning import Meaning
from .term_tech import TermTech


class Semantic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    meanings = models.ManyToManyField(Meaning, blank=True, related_name='semantic_meanings')
    term_techs = models.ManyToManyField(TermTech, blank=True, related_name='semantic_term_tech')
    comment = models.TextField(null=True, blank=True)
    history = HistoricalRecords()
    # TODO add pointers to taxonomy
