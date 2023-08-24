import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Optional
from treeflow.corpus import models

@strawberry_django.type(models.Corpus)
class Corpus(relay.Node):

    text_corpus: List[strawberry.LazyType['Text', 'treeflow.corpus.types.text']] = strawberry_django.field()

    id: relay.NodeID[str]
    name: strawberry.auto
    slug: strawberry.auto
