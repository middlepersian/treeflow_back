import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from .physical import Line
from mpcd.dict.models.dictionary import Entry


class Pos(models.TextChoices):
    ADJ = 'ADJ', 'Adjective'
    ADP = 'ADP', 'Adposition'
    ADV = "ADV", "Adverb"
    AUX = "AUX", "Auxiliary"
    CCONJ = "CCONJ", "Coordinating conjunction"
    DET = "DET", "Determiner"
    INTJ = "INTJ", "Interjection"
    NOUN = "NOUN", "Noun"
    NUM = "NUM", "Numeral"
    PART = "PART", "Particle"
    PRON = "PRON", "Pronoun"
    PROPN = "PROPN", "Proper noun"
    PUNCT = "PUNCT", "Punctuation"
    SCONJO = "SCONJO", "Subordinating conjunction"
    SYM = "SYM", "Symbol"
    VERB = "VERB", "Verb"
    X = "X", "Other"


class TokenSemantics(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    meaning = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class FeatureValueManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class FeatureValue(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    # e.g. 'Prs'
    name = models.SlugField(unique=True)
    # e.g. 'personal or possessive personal pronoun or determiner'
    value = models.CharField(max_length=150, unique=True)

    objects = FeatureValueManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'value'], name='featurevalue_name_value'
            )
        ]

    def __str__(self):
        return '{}'.format(self.name)


class FeatureManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Feature(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    # e.g. "PronType"
    name = models.CharField(max_length=20, unique=True)
    # e.g. "pronominal type"
    value = models.CharField(max_length=100, unique=True)

    objects = FeatureManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'value'], name='feature_name_value'
            )
        ]

    def __str__(self):
        return '{}'.format(self.name)


class MorphologicalAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    pos = models.CharField(max_length=6, choices=Pos.choices, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)
    feature_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_pos",
                check=models.Q(pos__in=Pos.values),
            ),
            models.UniqueConstraint(
                fields=['pos', 'feature', 'feature_value'], name='pos_feature_feature_value'
            )
        ]

    def __str__(self):
        return '{} {} {}'.format(self.pos, self.feature, self.feature_value)


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
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)

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
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.dependency)


class Token(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    token = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    lemma = models.ForeignKey(Entry, on_delete=models.DO_NOTHING, null=True, blank=True)

    morph_annotations = models.ForeignKey(MorphologicalAnnotation, on_delete=models.CASCADE, null=True, blank=True)
    syntax_annotations = models.ForeignKey(SyntacticAnnotation, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True)

    avestan = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.token


class CodexToken(Token):
    line_id = models.ForeignKey(Line, on_delete=models.CASCADE)
