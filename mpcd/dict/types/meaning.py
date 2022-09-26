
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.dict import models
from mpcd.corpus import types


@gql.django.type(models.Meaning)
class Meaning:
    id: gql.auto
    meaning: gql.auto
    language: gql.auto
    related_meanings: List['Meaning']
    comments : List['types.Comment']
