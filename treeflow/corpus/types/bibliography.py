import strawberry
import strawberry_django
from strawberry import relay
from treeflow.corpus import models

@strawberry_django.type(models.BibEntry)
class BibEntry(relay.Node):

    id: relay.NodeID[str]
    key: strawberry.auto

@strawberry_django.input(models.BibEntry)
class BibEntryInput:

    key: strawberry.auto

@strawberry_django.partial(models.BibEntry)
class BibEntryPartial:
    
    id: relay.GlobalID
    key: strawberry.auto