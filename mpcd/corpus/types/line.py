from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Comment, Folio


@gql.django.type(models.Line)
class Line:
    id: gql.auto
    number: gql.auto
    folio: 'Folio'
    comments: List[Comment]
    previous: 'Line'