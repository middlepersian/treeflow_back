import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .lemma import Lemma
from .reference import Reference
from .semantic import Semantic


# This is an "onomasiological" entry.
class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # In the setup of a multilingual onomasiological dictionary, there are multiple lemmas in different languages for the same entry
    lemmas = models.ManyToManyField(Lemma, blank=True, related_name="entry_lemmas")
    semantics = models.ManyToManyField(Semantic, blank=True, related_name="entry_semantics")
    references = models.ManyToManyField(Reference, blank=True, related_name='entry_references')
    related_entries = models.ManyToManyField('self', blank=True, related_name='entry_related_entries')
    comment = models.TextField(null=True, blank=True)

    history = HistoricalRecords()
