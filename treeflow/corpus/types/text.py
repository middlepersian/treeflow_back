from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from treeflow.corpus import models

if TYPE_CHECKING:
    from .token import Token
    from .section import Section
    from .corpus import Corpus
    from .text_sigle import TextSigle
    from .user import User
    from .source import Source
    from .bibliography import BibEntry


@gql.django.type(models.Text)
class Text(relay.Node):

    token_text: relay.Connection[gql.LazyType['Token',  'treeflow.corpus.types.token']]
    section_text: relay.Connection[gql.LazyType['Section',  'treeflow.corpus.types.section']]
    text_comment : relay.Connection[gql.LazyType['Comment',  'treeflow.corpus.types.comment']]

    # fields
    id: relay.GlobalID
    corpus: gql.LazyType['Corpus', 'treeflow.corpus.types.corpus']
    title: gql.auto
    text_sigle: gql.LazyType['TextSigle', 'treeflow.corpus.types.text_sigle']
    editors: List[gql.LazyType['User', 'treeflow.corpus.types.user']]
    collaborators: List[gql.LazyType['User', 'treeflow.corpus.types.user']]
    stage: gql.auto
    sources: List[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    resources: List[gql.LazyType['BibEntry',  'treeflow.corpus.types.bibliography']]


@gql.django.input(models.Text)
class TextInput:
    corpus: gql.auto
    title: gql.auto
    text_sigle: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: gql.auto
    resources: gql.auto


@gql.django.partial(models.Text)
class TextPartial(gql.NodeInputPartial):
    id: relay.GlobalID
    corpus: gql.auto
    title: gql.auto
    text_sigle: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: gql.auto
    resources: gql.auto
