from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Optional, List
from treeflow.corpus import models


@gql.django.type(models.Comment)
class Comment(relay.Node):
    id: relay.GlobalID
    user: Optional[gql.LazyType['User', 'treeflow.corpus.types.user']]
    comment: gql.auto
    created_at: gql.auto
    updated_at: gql.auto

    codex: Optional[gql.LazyType['Codex', 'treeflow.corpus.types.codex']]
    dependency: Optional[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    facsimile: Optional[gql.LazyType['Facsimile', 'treeflow.images.types.facsimile']]
    image: Optional[gql.LazyType['Image', 'treeflow.images.types.image']]
    section_type: Optional[gql.LazyType['SectionType', 'treeflow.corpus.types.section_type']]
    section: Optional[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    text_sigle: Optional[gql.LazyType['TextSigle', 'treeflow.corpus.types.text_sigle']]
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    token: Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.input(models.Comment)
class CommentInput:
    user: gql.auto
    comment: gql.auto

    codex:  gql.auto
    dependency:  gql.auto
    facsimile:  gql.auto
    image:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
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

    codex:  gql.auto
    dependency:  gql.auto
    facsimile:  gql.auto
    image:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
    text_sigle:  gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
