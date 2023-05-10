from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from treeflow.corpus import models
from treeflow.corpus.types.section import SectionFilter

@gql.django.filters.filter(models.Text)
class TextFilter:
    id: relay.GlobalID
    title: gql.auto


@gql.django.type(models.Text, filters=TextFilter)
class Text(relay.Node):

    token_text: relay.Connection[gql.LazyType['Token',  'treeflow.corpus.types.token']]
    section_text: relay.Connection[gql.LazyType['Section',  'treeflow.corpus.types.section']]
    text_comment : relay.Connection[gql.LazyType['Comment',  'treeflow.corpus.types.comment']]

    id: relay.GlobalID
    corpus: gql.LazyType['Corpus', 'treeflow.corpus.types.corpus']
    title: gql.auto
    series: gql.auto
    label: gql.auto
    version: gql.auto
    editors: List[gql.LazyType['User', 'treeflow.corpus.types.user']]
    collaborators: List[gql.LazyType['User', 'treeflow.corpus.types.user']]
    stage: gql.auto
    sources: List[gql.LazyType['Source', 'treeflow.corpus.types.source']]


@gql.django.input(models.Text)
class TextInput:
    corpus: gql.auto
    title: gql.auto
    version: gql.auto
    series: gql.auto
    label: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: gql.auto


@gql.django.partial(models.Text)
class TextPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    corpus: gql.auto
    title: gql.auto
    version : gql.auto
    series: gql.auto
    label: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: gql.auto
