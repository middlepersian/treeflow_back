from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import CommentCategory
from .comment_category_enum import CommentCategories
from graphql_jwt.decorators import login_required

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class CommentCategoryNode(DjangoObjectType):
    class Meta:
        model = CommentCategory
        filter_fields = ['category']
        interfaces = (relay.Node, )


class CommentCategoryInput(InputObjectType):
    category = CommentCategories(required=True)


class Query(ObjectType):
    comment_category = relay.Node.Field(CommentCategoryNode)
    comment_categories = DjangoFilterConnectionField(CommentCategoryNode)

    @login_required
    def resolve_comment_categories(self, info, **kwargs):
        return CommentCategory.objects.all()

    @login_required
    def resolve_comment_category(self, info, id):
        id = from_global_id(id)[1]
        return CommentCategory.objects.get(pk=id)
