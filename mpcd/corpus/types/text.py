from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional, Annotated
from mpcd.corpus import models

if TYPE_CHECKING:
    from .token import Token
    from .section import Section
    from .sentence import Sentence
    from .corpus import Corpus
    from .text_sigle import TextSigle
    from .user import User
    from .source import Source
    from .bibliography import BibEntry


@gql.django.type(models.Text)
class Text(relay.Node):

    token_text: relay.Connection[Annotated['Token',  lazy('mpcd.corpus.types.token')]]
    section_text: relay.Connection[Annotated['Section',  lazy('mpcd.corpus.types.section')]]
    sentence_text: relay.Connection[Annotated['Sentence',  lazy('mpcd.corpus.types.sentence')]]

    # fields
    id: gql.auto
    corpus: Annotated['Corpus', lazy('mpcd.corpus.types.corpus')]
    title: gql.auto
    text_sigle: Annotated['TextSigle', lazy('mpcd.corpus.types.text_sigle')]
    editors: List[Annotated['User', lazy('mpcd.corpus.types.user')]]
    collaborators: List[Annotated['User', lazy('mpcd.corpus.types.user')]]
    stage: gql.auto
    sources: List[Annotated['Source', lazy('mpcd.corpus.types.source')]]
    resources: List[Annotated['BibEntry',  lazy('mpcd.corpus.types.bibliography')]]


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
    id: gql.auto
    corpus: gql.auto
    title: gql.auto
    text_sigle: gql.auto
    editors: gql.auto
    collaborators: gql.auto
    stage: gql.auto
    sources: gql.auto
    resources: gql.auto
