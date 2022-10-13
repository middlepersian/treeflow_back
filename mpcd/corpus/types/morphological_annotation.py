from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING
from mpcd.corpus import models


@gql.django.type(models.MorphologicalAnnotation)
class MorphologicalAnnotation(relay.Node):
    id: gql.auto
    feature: gql.auto
    feature_value: gql.auto
