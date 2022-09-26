from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Comment, Facsimile


@gql.django.type(models.Line)
class Folio:
    id: gql.auto
    number: gql.auto
    facsimile: 'Facsimile'
    comments: List[Comment]
    previous: 'Folio'
