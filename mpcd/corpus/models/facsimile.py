import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from mpcd.corpus.models.bibliography import BibEntry
from mpcd.corpus.models.codex import Codex

class Facsimile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    bib_entry = models.OneToOneField(BibEntry, on_delete=models.SET_NULL, related_name='facsimile_reference', null=True)
    codex = models.ForeignKey(Codex, on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='facsimile_codex_part')

    history = HistoricalRecords()

    def __str__(self):
        return '{}'.format(self.bib_entry)
