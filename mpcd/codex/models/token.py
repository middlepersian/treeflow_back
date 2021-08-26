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


class FeatureValue(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    # e.g. 'Prs'
    slug = models.SlugField(unique=True)
    # e.g. 'personal or possessive personal pronoun or determiner'
    description = models.CharField(max_length=150)

class Feature(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    # e.g. "PronType"
    name = models.CharField(max_length=20)
    # e.g. "pronominal type"
    description = models.CharField(max_length=150)
    
    values = models.ManyToManyField(FeatureValue, blank=True, null=True)

class MorphologicalAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    pos = models.CharField(max_length=6, choices=Pos.choices, null=True)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, null=True)    
 
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_pos_valid",
                check=models.Q(pos__in=Pos.values),
            )]


    def __str__(self):
        return self.pos


        
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

class Dependency(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    head = models.SmallIntegerField()
    
    dependency_relation = models.CharField(max_length=9, choices=DependencyRelation.choices)

    def __str__(self):
        return str(self.head) + '    ' + self.dependency_relation


class SyntacticAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.dependency.head) + '    ' + self.dependency.dependency_relation


class Token(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    token = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    lemma = models.ForeignKey(Entry, on_delete=models.DO_NOTHING, null=True, blank=True)

    morph_annotations = models.ForeignKey(MorphologicalAnnotation, on_delete=models.CASCADE, null=True)
    syntax_annotations = models.ForeignKey(SyntacticAnnotation, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True)

    avestan = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.token


class CodexToken(Token):
    line_id = models.ForeignKey(Line, on_delete=models.CASCADE)
