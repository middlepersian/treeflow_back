from typing import List
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


from mpcd.corpus.types.comment import Comment


@gql.type
class Query:
    comments: relay.Connection[Comment] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
