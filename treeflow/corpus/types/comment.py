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

    dependency: Optional[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    image: Optional[gql.LazyType['Image', 'treeflow.images.types.image']]
    section_type: Optional[gql.LazyType['SectionType', 'treeflow.corpus.types.section_type']]
    source: Optional[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    section: Optional[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    token: Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.input(models.Comment)
class CommentInput:
    user: gql.auto
    comment: gql.auto

    dependency:  gql.auto
    image:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
    source: gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.partial(models.Comment)
class CommentPartial(gql.NodeInputPartial):
    user: gql.auto
    comment: gql.auto

    dependency:  gql.auto
    image:  gql.auto
    section_type:  gql.auto
    section:  gql.auto
    source: gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
