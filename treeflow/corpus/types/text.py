import strawberry
import strawberry_django
from strawberry import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from treeflow.corpus import models
from strawberry_django.relay import ListConnectionWithTotalCount
from treeflow.corpus.enums.text_stage import TextStage

@strawberry_django.filters.filter(models.Text)
class TextFilter:
    id: Optional[relay.GlobalID]
    title: strawberry.auto


@strawberry_django.type(models.Text, filters=Optional[TextFilter])
class Text(relay.Node):

    token_text: List[strawberry.LazyType['Token',  'treeflow.corpus.types.token']] = strawberry_django.field()
    section_text: List[strawberry.LazyType['Section',  'treeflow.corpus.types.section']] = strawberry_django.field()
    comment_text : List[strawberry.LazyType['Comment',  'treeflow.corpus.types.comment']] = strawberry_django.field()

    id: relay.NodeID[str]
    corpus: strawberry.LazyType['Corpus', 'treeflow.corpus.types.corpus']
    title: strawberry.auto
    identifier: strawberry.auto
    series: strawberry.auto
    label: strawberry.auto
    version: strawberry.auto
    editors: List[strawberry.LazyType['User', 'treeflow.corpus.types.user']]
    collaborators: List[strawberry.LazyType['User', 'treeflow.corpus.types.user']]
    stage: Optional[TextStage]
    sources: List[strawberry.LazyType['Source', 'treeflow.corpus.types.source']]


@strawberry_django.input(models.Text)
class TextInput:
    corpus: strawberry.auto
    title: strawberry.auto
    identifier: strawberry.auto
    series: strawberry.auto
    label: strawberry.auto
    version: strawberry.auto
    editors: strawberry.auto
    collaborators: strawberry.auto
    stage: Optional[TextStage]
    sources: strawberry.auto


@strawberry_django.partial(models.Text)
class TextPartial(strawberry_django.NodeInputPartial):
    
    id: relay.NodeID[str]
    corpus: strawberry.auto
    title: strawberry.auto
    identifier: strawberry.auto
    series: strawberry.auto
    label: strawberry.auto
    version : strawberry.auto
    editors: strawberry.auto
    collaborators: strawberry.auto
    stage: Optional[TextStage]
    sources: strawberry.auto
