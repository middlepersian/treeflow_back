import uuid as uuid_lib
from django.db import models


class DependencyRelation(models.TextChoices):
    acl = 'acl', 'clausal modifier of noun (adnominal clause)'
    advcl = 'advcl', 'adverbial clause modifier'
    advmod = "advmod", "adverbial modifier"
    amod = "amod", "adjectival modifier"
    appos = "appos", "appositional modifier"
    aux = "aux", "auxiliary"
    case = "case", "case marking"
    cc = "cc", "coordinating conjunction"
    ccomp = "ccomp", "clausal complement"
    compound = "compound", "compound"
    conj = "conj", "conjunct"
    cop = "cop", "copula"
    det = "det", "determiner"
    discourse = "discourse", "discourse element"
    fixed = "fixed", "fixed multiword expression"
    iobj = "iobj", "indirect object"
    mark = "mark", "marker"
    nmod = "nmod", "nominal modifier"
    nsubj = "nsubj", "nominal subject"
    nummod = "nummod", "numeric modifier"
    obj = "obj", "object"
    obl = "obl", "oblique nominal"
    root = "root", "root"


class DependencyManager(models.Manager):
    def get_by_natural_key(self, head, rel):
        return self.get(head=head, rel=rel)


class Dependency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)

    head = models.PositiveSmallIntegerField()
    rel = models.CharField(max_length=9, choices=DependencyRelation.choices)

    objects = DependencyManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_rel",
                check=models.Q(rel__in=DependencyRelation.values),
            ),
            models.UniqueConstraint(
                fields=['head', 'rel'], name='head_rel'
            )
        ]

    def __str__(self):
        return '{} {}'.format(str(self.head), self.rel)
