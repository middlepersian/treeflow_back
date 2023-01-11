from strawberry import lazy
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import TYPE_CHECKING, Annotated, Optional, List
from mpcd.corpus import models

if TYPE_CHECKING:
    from .user import User


@gql.django.type(models.Comment)
class Comment(relay.Node):
    id: relay.GlobalID
    user: Optional[gql.LazyType['User', 'mpcd.corpus.types.user']]
    comment: gql.auto
    created_at: gql.auto
    updated_at: gql.auto

    codex_part: Optional[gql.LazyType['CodexPart', 'mpcd.corpus.types.codex_part']]
    codex: Optional[gql.LazyType['Codex', 'mpcd.corpus.types.codex']]
    dependency: Optional[gql.LazyType['Dependency', 'mpcd.corpus.types.dependency']]
    #edition: Optional[gql.LazyType['Edition', 'mpcd.corpus.types.edition']]
    facsimile: Optional[gql.LazyType['Facsimile', 'mpcd.corpus.types.facsimile']]
    folio: Optional[gql.LazyType['Folio', 'mpcd.corpus.types.folio']]
    line: Optional[gql.LazyType['Line', 'mpcd.corpus.types.line']]
    section_type: Optional[gql.LazyType['SectionType', 'mpcd.corpus.types.section_type']]
    section: Optional[gql.LazyType['Section', 'mpcd.corpus.types.section']]
    sentence: Optional[gql.LazyType['Sentence', 'mpcd.corpus.types.sentence']]
    text_sigle: Optional[gql.LazyType['TextSigle', 'mpcd.corpus.types.text_sigle']]
    text: Optional[gql.LazyType['Text', 'mpcd.corpus.types.text']]
    token: Optional[gql.LazyType['Token', 'mpcd.corpus.types.token']]

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.input(models.Comment)
class CommentInput:
    user: gql.auto
    comment: gql.auto

    codex_part:  gql.auto
    codex:  gql.auto
    dependency:  gql.auto
    #edition: Optional[gql.LazyType['Edition', 'mpcd.corpus.types.edition']]
    facsimile:  gql.auto
    folio:  gql.auto
    line:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
    sentence:  gql.auto
    text_sigle:  gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.partial(models.Comment)
class CommentPartial(gql.NodeInputPartial):
    user: gql.auto
    comment: gql.auto

    codex_part:  gql.auto
    codex:  gql.auto
    dependency:  gql.auto
    #edition: Optional[gql.LazyType['Edition', 'mpcd.corpus.types.edition']]
    facsimile:  gql.auto
    folio:  gql.auto
    line:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
    sentence:  gql.auto
    text_sigle:  gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
