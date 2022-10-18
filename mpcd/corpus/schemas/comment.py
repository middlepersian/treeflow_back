from typing import Optional
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


from mpcd.corpus.types.comment import Comment


@gql.type
class Query:
    comment: Optional[Comment] = gql.django.node()
    comments: relay.Connection[Comment] = gql.django.connection()


schema = gql.Schema(query=Query, extensions=[DjangoOptimizerExtension])
