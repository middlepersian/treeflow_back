import uuid as uuid_lib

from django.db import models
from django.urls import reverse
from physical import Line


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
            ('Nom', 'Nom)'),
            ('Acc', 'Acc)'),
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
            ('Def', 'Def')
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
        ))
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


class Token(models.Model):
    uuid = models.UUIDField(default=uuid_lib.uuid4, editable=False)
    line_id = models.ForeignKey(Line, on_delete=models.SET_NULL)
    tkn = models.CharField(max_length=255)
    trascription = models.TextField(blank=True)
    transliteration = models.TextField(blank=True)
    lemma = models.ForeignKey()

    morph_annotations = models.ForeignKey(MorphologicalAnnotation, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    comment = models.TextField(blank=True)

    avestan = models.CharField(max_length=255, blank=True)
