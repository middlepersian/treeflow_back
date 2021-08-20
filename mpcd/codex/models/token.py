import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from .physical import Line


class TokenSemantics(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)
    meaning = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class MorphologicalAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False, unique=True)

    ADJ_FEATURES = [
        ('NumType', (
            ('Ord', 'Ord'),
            ('Mult', 'Mult'),
        )),
        ('Poss', (
            ('Yes', 'Yes)'),
        )),
        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur'),
        )),
        ('Case', (
            ('Nom', 'Nom'),
            ('Acc', 'Acc'),
        )),
        ('Degree', (
            ('Cmp', 'Cmp'),
            ('Pos', 'Pos'),
            ('Sup', 'Sup')
        )),
        ('VerbForm', (
            ('Part', 'Part'))),
        ('Tense', (
            ('Past', 'Past'),
            ('Pres', 'Pres'),
        )),
        ('Voice', (
            ('Act', 'Act'),
            ('Pass', 'Pass'),
            ('Cau', 'Cau')
        )),
        ('Polarity', (
            ('Neg', 'Neg')
        ))
    ]

    ADP_FEATURES = [

        ('Pos', (
            ('Pre', 'Pre'),
            ('Post', 'Post'),
            ('Circum', 'Circum')
        ))

    ]

    ADV_FEATURES = [

        ('PronType', (
            ('Dem', 'Dem'),
            ('Ind', 'Ind'),
            ('Int', 'Int'),
            ('Neg', 'Neg'),
            ('Rel', 'Rel'),
            ('Tot', 'Tot')
        )),
        ('NumType', (
            ('Ord', 'Ord)'),
            ('Mult', 'Mult)'),
        )),

        ('Degree', (
            ('Cmp', 'Cmp'),
            ('Pos', 'Pos'),
            ('Sup', 'Sup')
        )),
        ('VerbForm', (
            ('Part', 'Part')
        )),
        ('Tense', (
            ('Past', 'Past'),
            ('Pres', 'Pres')
        )),
        ('Voice', (
            ('Act', 'Act'),
            ('Pass', 'Pass'),
            ('Cau', 'Cau')
        )),
        ('Polarity', (
            ('Neg', 'Neg')
        ))

    ]

    AUX_FEATURES = [

        ('Copula', (
            ('Yes', 'Yes')
        )),
        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur'),
        )),

        ('VerbForm', (
            ('Fin', 'Fin'),
            ('Inf', 'Inf'),
            ('Part', 'Part')
        )),
        ('Mood', (
            ('Part', 'Part')
        )),
        ('Tense', (
            ('Past', 'Past'),
            ('Pres', 'Pres')
        )),
        ('Voice', (
            ('Act', 'Act'),
            ('Pass', 'Pass'),
            ('Cau', 'Cau')
        )),
        ('Polarity', (
            ('Neg', 'Neg')
        )),
        ('Person', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
        )),
        ('Polite', (
            ('Form', 'Form')
        ))
    ]

    DET_FEATURES = [
        ('PronType', (
            ('Dem', 'Dem'),
            ('Emp', 'Emp'),
            ('Exc', 'Exc'),
            ('Ind', 'Ind'),
            ('Int', 'Int'),
            ('Neg', 'Neg'),
            ('Rel', 'Rel'),
            ('Tot', 'Tot')
        )),
        ('Poss', (
            ('Yes', 'Yes')
        )),

        ('Reflex', (
            ('Yes', 'Yes')
        )),
        ('Number', (
            ('Sing', 'Sing'),
            ('Plural', 'Plural')
        ))

    ]

    NOUN_FEATURES = [

        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur')
        )),
        ('Case', (
            ('Nom', 'Nom'),
            ('Acc', 'Acc'),
        )),

        ('Definite', (
            ('Ind', 'Ind'),
            ('Spec', 'Spec'),
            ('Def', 'Def')
        )),
        ('VerbForm', (
            ('Part', 'Part'),
            ('Inf', 'Inf'),
            ('Vnoun', 'Vnoun')
        )),
        ('Tense', (
            ('Past', 'Past'),
            ('Pres', 'Pres')
        )),
        ('Voice', (
            ('Act', 'Act'),
            ('Pass', 'Pass'),
            ('Cau', 'Cau')
        )),
        ('Polarity', (
            ('Neg', 'Neg')
        )),
        ('Animacy', (
            ('Hum', 'Hum'), ('Spec', 'Spec'),
            ('Def', 'Def'),
            ('Nhum', 'Nhum'),
            ('Anim', 'Anim'),
            ('Inan', 'Inan')
        ))

    ]

    NUM_FEATURES = [

        ('PronType', (
            ('Dem', 'Dem'),
            ('Ind', 'Ind'),
            ('Int', 'Int'),
            ('Rel', 'Rel')
        )),
        ('NumType', (
            ('Card', 'Card'),
            ('Frac', 'Frac'),
            ('Sets', 'Sets'),
        )),
        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur')
        ))

    ]

    PART_FEATURES = [
        ('PartType', (
            ('Verbal', 'Verbal'),
            ('Poss', 'Poss'),
            ('Neg', 'Neg'),
        ))

    ]

    PRON_FEATURES = [

        ('PronType', (
            ('Dem', 'Dem'),
            ('Emp', 'Emp'),
            ('Exc', 'Exc'),
            ('Ind', 'Ind'),
            ('Int', 'Int'),
            ('Neg', 'Neg'),
            ('Rel', 'Rel'),
            ('Tot', 'Tot')
        )),
        ('Poss', (
            ('Yes', 'Yes')
        )),

        ('Reflex', (
            ('Yes', 'Yes')
        )),
        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur')
        )),
        ('Person', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
        )),
        ('Polite', (
            ('Form', 'Form')
        ))

    ]

    PUNCT_FEATURES = [
        ('Type', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('etc', 'etc')
        ))

    ]

    VERB_FEATURES = [

        ('Number', (
            ('Sing', 'Sing'),
            ('Plur', 'Plur')
        )),
        ('VerbForm', (
            ('Fin', 'Fin'),
            ('Inf', 'Inf'),
            ('Part', 'Part')
        )),
        ('Mood', (
            ('Ind', 'Imp'),
            ('Imp', 'Imp'),
            ('Sub', 'Sub'),
            ('Opt', 'Opt')

        )),
        ('Tense', (
            ('Past', 'Past'),
            ('Pres', 'Pres')
        )),
        ('Voice', (
            ('Act', 'Act'),
            ('Pass', 'Pass'),
            ('Cau', 'Cau')
        )),
        ('Person', (
            ('1', '1'),
            ('2', '2'),
            ('3', '3')
        )),
        ('Polite', (
            ('Form', 'Form')
        ))

    ]

    X_FEATURES = [
        ('Foreign', ('Yes', 'Yes'))
    ]

    class PosTag(models.TextChoices):
        ADJ = 'ADJ', 'Adjective'
        ADP = 'ADP', 'Adposition'
        ADV = "ADV", "Adverb"
        AUX = "AUX", "auxiliary"
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

    pos_tag = models.CharField(max_length=6, choices=PosTag.choices)


    # get current pos_tag for setting the right pos_features
    '''
    @classmethod
    def pos_value(self):
         return self.pos_tag

    if pos_value() == 'ADJ':
        features = ADJ_FEATURES
    elif pos_value() == 'ADV':
        features = ADV_FEATURES
    elif pos_value() == 'ADP':
        features = ADP_FEATURES
    elif pos_value() == 'AUX':
        features = AUX_FEATURES
    elif pos_value() == 'DET':
        features = DET_FEATURES
    elif pos_value() == 'NOUN':
        features = NOUN_FEATURES
    elif pos_value() == 'NUM':
        features = NUM_FEATURES
    elif pos_value() == 'PART':
        features = PART_FEATURES
    elif pos_value() == 'PRON':
        features = PRON_FEATURES
    elif pos_value() == 'PUNCT':
        features = PUNCT_FEATURES
    elif pos_value() == 'VERB':
        features = VERB_FEATURES
    elif pos_value() == 'X':
        features = X_FEATURES

    if features:
        pos_features = models.ArrayField(models.CharField(max_length=20, choices=features), null=True, blank=True)
    '''


class Dependency(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    head = models.SmallIntegerField()
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

    dependency_relation = models.CharField(max_length=9, choices=DependencyRelation.choices)


class SyntacticAnnotation(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    dependency = models.ForeignKey(Dependency, on_delete=models.CASCADE, null=True, blank=True)


class Token(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    tkn = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    #lemma = models.ForeignKey()

    morph_annotations = models.ForeignKey(MorphologicalAnnotation, on_delete=models.CASCADE, null=True)
    syntax_annotations = models.ForeignKey(SyntacticAnnotation, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True)

    avestan = models.CharField(max_length=255, blank=True)


class CodexToken(Token):
    line_id = models.ForeignKey(Line, on_delete=models.
    CASCADE)
