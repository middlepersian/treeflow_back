from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from treeflow.corpus import models

@gql.django.type(models.Codex)
class Codex(relay.Node):
    id: relay.GlobalID
    facsimile_codex: relay.Connection[gql.LazyType['Facsimile', 'treeflow.images.types.facsimile']]

    sigle: gql.auto
