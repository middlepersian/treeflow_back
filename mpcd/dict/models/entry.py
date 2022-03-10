from platform import release
import uuid as uuid_lib
from django.db import models
from simple_history.models import HistoricalRecords
from .dictionary import Dictionary
from .lemma import Lemma
from .loanword import LoanWord
from .translation import Translation
from .definition import Definition
from .category import Category
from .reference import Reference


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dict = models.ForeignKey(Dictionary, on_delete=models.CASCADE, blank=True, related_name='entry_dict')
    lemma = models.OneToOneField(Lemma, on_delete=models.CASCADE, related_name="entry_lemma")
    loanwords = models.ManyToManyField(LoanWord, blank=True, related_name='entry_loanwords')
    translations = models.ManyToManyField(Translation, blank=True, related_name='entry_translations')
    definitions = models.ManyToManyField(Definition, blank=True, related_name='entry_definitions')
    categories = models.ManyToManyField(Category, blank=True, related_name='entry_categories')
    references = models.ManyToManyField(Reference, blank=True, related_name='entry_references')
    related_entries = models.ManyToManyField('self', blank=True, related_name='entry_related_entries')
    comment = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['lemma__word']

    def __str__(self):
        return '{}'.format(self.lemma)
