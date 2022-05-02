import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

from .meaning import Meaning
from .term_tech import TermTech
from .entry import Entry


class Semantic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    entry = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True, related_name="semantic_entry")
    meanings = models.ManyToManyField(Meaning, blank=True, related_name='semantic_meanings')
    term_techs = models.ManyToManyField(TermTech, blank=True, related_name='semantic_term_techs')
    comment = models.TextField(null=True, blank=True)
    history = HistoricalRecords()
    # TODO add pointers to taxonomy
