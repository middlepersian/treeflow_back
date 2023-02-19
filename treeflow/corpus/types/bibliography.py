from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from treeflow.corpus import models

@gql.django.type(models.BibEntry)
class BibEntry(relay.Node):
    id: relay.GlobalID
    key: gql.auto

@gql.django.input(models.BibEntry)
class BibEntryInput:
    key: gql.auto

@gql.django.partial(models.BibEntry)
class BibEntryPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    key: gql.auto