from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import Optional, List
from treeflow.corpus import models

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    IsAuthenticated,
     IsSuperuser,
)

@gql.django.type(models.Comment)
class Comment(relay.Node):
    id: relay.GlobalID
    comment: gql.auto  
    user : Optional[gql.LazyType('User', 'treeflow.corpus.types.user')] = gql.django.field(directives=[IsSuperuser()])

    dependency: Optional[gql.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    image: Optional[gql.LazyType['Image', 'treeflow.images.types.image']]
    source: Optional[gql.LazyType['Source', 'treeflow.corpus.types.source']]
    section: Optional[gql.LazyType['Section', 'treeflow.corpus.types.section']]
    text: Optional[gql.LazyType['Text', 'treeflow.corpus.types.text']]
    token: Optional[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.input(models.Comment)
class CommentInput:
    comment: gql.auto

    user : gql.auto
    dependency:  gql.auto
    image:  gql.auto
    section:  gql.auto
    source: gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]


@gql.django.partial(models.Comment)
class CommentPartial(gql.NodeInputPartial):
    comment: gql.auto

    user: gql.auto
    dependency:  gql.auto
    image:  gql.auto
    section:  gql.auto
    source: gql.auto
    text:  gql.auto
    token:  gql.auto

    uncertain: Optional[List[Optional[str]]]
    to_discuss: Optional[List[Optional[str]]]
    new_suggestion:  Optional[List[Optional[str]]]
