
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Dependency, Text, TokenComment, Line, MorphologicalAnnotation
from mpcd.dict.types import Lemma, Meaning


@gql.django.type(models.Token)
class Token:
    id: gql.auto
    number: gql.auto
    text: 'Text'
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List[Lemma]
    meanings: List[Meaning]
    pos: gql.auto
    morphological_annotation: List['MorphologicalAnnotation']
    syntactic_annotation: List[Dependency]
    comments: List[TokenComment]
    avestan: gql.auto
    line: 'Line'
    previous: 'Token'
    gloss: gql.auto


@gql.django.input(models.Token)
class TokenInput:
    id: gql.auto
    number: gql.auto
    text: 'Text'
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List['Lemma']
    meanings: List['Meaning']
    pos: gql.auto
    morphological_annotation: List['MorphologicalAnnotation']
    syntactic_annotation: List['Dependency']
    comments: List['TokenComment']
    avestan: gql.auto
    line: 'Line'
    previous: 'Token'
    gloss: gql.auto


@gql.django.partial(models.Token)
class TokenInputPartial(gql.NodeInput):
    id: gql.auto
    number: gql.auto
    text: 'Text'
    language: gql.auto
    transcription: gql.auto
    transliteration: gql.auto
    lemmas: List['Lemma']
    meanings: List['Meaning']
    pos: gql.auto
    morphological_annotation: List['MorphologicalAnnotation']
    syntactic_annotation: List['Dependency']
    comments: List['TokenComment']
    avestan: gql.auto
    line: 'Line'
    previous: 'Token'
    gloss: gql.auto
