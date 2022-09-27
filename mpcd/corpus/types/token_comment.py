from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models


@gql.django.type(models.TokenComment)
class TokenComment:
    uncertain: List[str]
    to_discuss: List[str]
    new_suggestion: List[str]
