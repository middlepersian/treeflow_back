import uuid as uuid_lib
from django.db import models




class Semantic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # This should ideally a 1:1 relationship with a lemma, but we don't know it.
    #lemmas = models.ManyToManyField('Lemma', blank=True, related_name='semantic_lemmas')
    # Multimlingual setup: there are multiple meanings in different languages for the same semantic
    #meanings = models.ManyToManyField('Meaning', blank=True, related_name='semantic_meanings')
    #term_techs = models.ManyToManyField(TermTech, blank=True, related_name='semantic_term_techs')
    related_semantics = models.ManyToManyField('self', blank=True)


    # TODO add pointers to taxonomy
