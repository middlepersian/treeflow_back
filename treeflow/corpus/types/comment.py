import strawberry
import strawberry_django
from strawberry import relay
from strawberry_django.fields.types import NodeInputPartial
from strawberry_django.permissions import IsAuthenticated, IsSuperuser

from typing import Optional, List
from treeflow.corpus import models
from treeflow.corpus.enums.comment_categories import CommentCategories

@strawberry_django.type(models.Comment)
class Comment(relay.Node):
    
    id: relay.NodeID[str]
    comment: strawberry.auto  
    user : Optional[strawberry.LazyType('User', 'treeflow.corpus.types.user')] = strawberry_django.field(extensions=[IsSuperuser()])

    dependency: Optional[strawberry.LazyType['Dependency', 'treeflow.corpus.types.dependency']]
    image: Optional[strawberry.LazyType['Image', 'treeflow.images.types.image']]
    source: Optional[strawberry.LazyType['Source', 'treeflow.corpus.types.source']]
    section: Optional[strawberry.LazyType['Section', 'treeflow.corpus.types.section']]
    text: Optional[strawberry.LazyType['Text', 'treeflow.corpus.types.text']]
    token: Optional[strawberry.LazyType['Token', 'treeflow.corpus.types.token']]

    created_at: strawberry.auto

    uncertain: Optional[List[Optional[CommentCategories]]]
    to_discuss: Optional[List[Optional[CommentCategories]]]
    new_suggestion: Optional[List[Optional[CommentCategories]]]


@strawberry_django.input(models.Comment)
class CommentInput:
    comment: strawberry.auto

    user : strawberry.auto
    dependency:  strawberry.auto
    image:  strawberry.auto
    section:  strawberry.auto
    source: strawberry.auto
    text:  strawberry.auto
    token:  strawberry.auto

    uncertain: Optional[List[Optional[CommentCategories]]]
    to_discuss: Optional[List[Optional[CommentCategories]]]
    new_suggestion: Optional[List[Optional[CommentCategories]]]


@strawberry_django.partial(models.Comment)
class CommentPartial(NodeInputPartial):
    id: relay.NodeID[str]

    comment: strawberry.auto

    user: strawberry.auto
    dependency:  strawberry.auto
    image:  strawberry.auto
    section:  strawberry.auto
    source: strawberry.auto
    text:  strawberry.auto
    token:  strawberry.auto

    uncertain: Optional[List[Optional[CommentCategories]]]
    to_discuss: Optional[List[Optional[CommentCategories]]]
    new_suggestion: Optional[List[Optional[CommentCategories]]]


@strawberry_django.type
class CommentCategoriesList:
    categories : List[CommentCategories]
    