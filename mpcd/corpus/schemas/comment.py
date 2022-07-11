from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from mpcd.corpus.models import Comment
from mpcd.corpus.schemas.comment_category_enum import CommentCategories

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        filter_fields = ['text']
        interfaces = (relay.Node, )


class CommentInput(InputObjectType):
    user = ID
    categories = List(CommentCategories, required=false)
    text = String(required=True)


class Query(ObjectType):
    comment = relay.Node.Field(CommentNode)
    comments = DjangoFilterConnectionField(CommentNode)

    @login_required
    def resolve_comments(self, info, **kwargs):
        qs = Comment.objects.all()
        return gql_optimizer.query(qs, info)

    @login_required
    def resolve_comment(self, info, id):
        id = from_global_id(id)[1]
        return Comment.objects.get(pk=id)

# Mutations


class CreateComment(relay.ClientIDMutation):
    class Input:
        user = ID
        categories = List(CommentCategories, required=false)
        text = String(required=True)

    comment = Field(CommentNode)
    errors = List(String)
    success = Boolean()

    @login_required
    def mutate_and_get_payload(root, info, user, categories, text):
        comment_obj, comment_created = Comment.objects.getr_ot_create(user=user, categories=categories, text=text)
        return cls(comment=comment_obj, success=True, errors=None)
