from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional

from treeflow.corpus import models

import strawberry


@gql.django.type(models.POS)
class POS(relay.Node):
    id: relay.GlobalID
    token : gql.LazyType['Token', 'treeflow.corpus.types.token']
    pos: gql.auto
    type: gql.auto


@gql.django.input(models.POS)
class POSInput:
    token : gql.auto
    pos: gql.auto
    type: gql.auto

@gql.django.partial(models.POS)
class POSPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    token: gql.auto
    pos: gql.auto
    type: gql.auto
