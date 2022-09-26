
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.dict import models
from mpcd.dict.types import Meaning
from mpcd.corpus import types as corpus_types



@gql.django.type(models.Lemma)
class Lemma:
    id: gql.auto
    word: gql.auto
    language: gql.auto
    related_lemmas: List['Lemma']
    related_meanings : List['Meaning']
    comments: List ['corpus_types.Comment']