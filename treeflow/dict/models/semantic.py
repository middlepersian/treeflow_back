import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords

from .meaning import Meaning
from treeflow.corpus.models.comment import Comment

from .term_tech import TermTech
from treeflow.dict.models import Lemma


class Semantic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # This should ideally a 1:1 relationship with a lemma, but we don't know it.
    lemmas = models.ManyToManyField(Lemma, blank=True, related_name='semantic_lemmas')
    # Multimlingual setup: there are multiple meanings in different languages for the same semantic
    meanings = models.ManyToManyField(Meaning, blank=True, related_name='semantic_meanings')
    term_techs = models.ManyToManyField(TermTech, blank=True, related_name='semantic_term_techs')
    related_semantics = models.ManyToManyField('self', blank=True)
    history = HistoricalRecords()
    # TODO add pointers to taxonomy
