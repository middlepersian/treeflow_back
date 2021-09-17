import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from mpcd.dict.models.dictionary import Entry
from simple_history.models import HistoricalRecords


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


class FeatureValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # e.g. 'Prs'
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class Feature(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    # e.g. "PronType"
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return '{}'.format(self.name)


class MorphologicalAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True, blank=True)
    feature_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['feature', 'feature_value'], name='feature_featurevalue'
            )
        ]

    def __str__(self):
        return '{} {}'.format(self.feature, self.feature_value)


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
    # TODO: add DB constraint
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


class SyntacticAnnotation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.dependency)


class Pos(models.Model):
    pos = models.CharField(max_length=6, choices=PosCh.choices, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_pos",
                check=models.Q(pos__in=PosCh.values),
            )]

    def __str__(self):
        return '{}'.format(self.pos)


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    transcription = models.CharField(max_length=50)
    transliteration = models.CharField(max_length=50, blank=True)
    lemma = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True, blank=True)
    pos = models.ForeignKey(Pos, on_delete=models.CASCADE, null=True)
    features = models.ManyToManyField(MorphologicalAnnotation, blank=True)
    syntax_annotations = models.ForeignKey(SyntacticAnnotation, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(blank=True)
    avestan = models.URLField(max_length=100, null=True, blank=True)
    previous = models.OneToOneField('self',
                                    related_name='previous_token',
                                    blank=True,
                                    null=True,
                                    on_delete=models.DO_NOTHING)

    history = HistoricalRecords()

    def ms_features(self):
        return "|\n".join([p.feature.name + '=' + p.feature_value.name for p in self.features.all()])

    def __str__(self):
        return '{}'.format(self.transcription)
