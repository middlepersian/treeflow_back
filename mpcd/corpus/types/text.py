
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING, Optional
from mpcd.corpus import models


@gql.django.type(models.Text)
class Text(relay.Node):

    token_text: relay.Connection[LazyType['Token', 'mpcd.corpus.types.token']]
    section_text: relay.Connection[LazyType['Section', 'mpcd.corpus.types.section']]
    sentence_text: relay.Connection[LazyType['Sentence', 'mpcd.corpus.types.sentence']]

    # fields
    id: gql.auto
    corpus: LazyType['Corpus', 'mpcd.corpus.types.corpus']
    title: gql.auto
    text_sigle: LazyType['TextSigle', 'mpcd.corpus.types.text_sigle']
    editors: List[LazyType['User', 'mpcd.corpus.types.user']]
    collaborators: List[LazyType['User', 'mpcd.corpus.types.user']]
    stage: gql.auto
    sources: List[LazyType['Source', 'mpcd.corpus.types.source']]
    resources: List[LazyType['BibEntry', 'mpcd.corpus.types.bibliography']]


@gql.django.input(models.Text)
class TextInput:
    corpus: gql.auto
    title: gql.auto
    text_sigle: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: Optional[List[LazyType['SourceInput', 'mpcd.corpus.types.source']]]
    resources: Optional[List[LazyType['BibEntryInput', 'mpcd.corpus.types.bibliography']]]


@gql.django.partial(models.Text)
class TextPartial(gql.NodeInputPartial):
    id: gql.auto
    corpus: gql.auto
    title: gql.auto
    text_sigle: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: Optional[List[LazyType['SourcePartial', 'mpcd.corpus.types.source']]]
    resources: Optional[List[LazyType['BibEntryPartial', 'mpcd.corpus.types.bibliography']]]
