from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from mpcd.corpus.types import Comment


@gql.django.type(models.Codex)
class Codex:
    sigle: gql.auto
    comments: List['Comment']
