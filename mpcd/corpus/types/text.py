
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING
from mpcd.corpus import models

if TYPE_CHECKING:
    from mpcd.corpus.types.corpus import Corpus
    from mpcd.corpus.types.text_sigle import TextSigle
    from mpcd.corpus.types.user import User
    from mpcd.corpus.types.source import Source
    from mpcd.corpus.types.bibliography import BibEntry
    from mpcd.corpus.types.token import Token


@gql.django.type(models.Text)
class Text(relay.Node):
    id: gql.auto
    corpus: LazyType['Corpus', 'mpcd.corpus.types.corpus']
    title: gql.auto
    text_sigle: LazyType['TextSigle', 'mpcd.corpus.types.text_sigle']
    editors: List[LazyType['User', 'mpcd.corpus.types.user']]
    token_text: List[LazyType['Token', 'mpcd.corpus.types.token']]
    collaborators: List[LazyType['User', 'mpcd.corpus.types.user']]
    stage: gql.auto
    sources: List[LazyType['Source', 'mpcd.corpus.types.source']]
    resources: List[LazyType['BibEntry', 'mpcd.corpus.types.bibliography']]
