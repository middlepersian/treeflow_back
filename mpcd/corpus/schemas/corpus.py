from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional
from mpcd.corpus.types.corpus import Corpus

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    corpus: Optional[Corpus] = gql.django.node(directives=[IsAuthenticated()])
    corpora:  relay.Connection[Corpus] = gql.django.connection(directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
