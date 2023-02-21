import uuid as uuid_lib
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


from .term_tech import TermTech


class Semantic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # This should ideally a 1:1 relationship with a lemma, but we don't know it.
    #lemmas = models.ManyToManyField('Lemma', blank=True, related_name='semantic_lemmas')
    # Multimlingual setup: there are multiple meanings in different languages for the same semantic
    #meanings = models.ManyToManyField('Meaning', blank=True, related_name='semantic_meanings')
    #term_techs = models.ManyToManyField(TermTech, blank=True, related_name='semantic_term_techs')
    related_semantics = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # TODO add pointers to taxonomy
