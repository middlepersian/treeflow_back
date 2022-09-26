
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Comment, Token

@gql.django.type(models.Dependency)
class Dependency:
    id: gql.auto
    head : 'Token'
    rel: gql.auto
    producer: gql.auto
    comments: List['Comment']