from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import CommentCategory
from .comment_category_enum import CommentCategories
from graphql_jwt.decorators import login_required


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


class CreateCommentCategory(relay.ClientIDMutation):
    class Input:
        category = CommentCategories(required=True)

    comment_category = Field(CommentCategoryNode)
    success = Boolean()
    errors = List(String)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        comment_category_obj, comment_category_created = CommentCategory.get_or_create(category=input.get('category'))
        return cls(comment_category=comment_category_obj, success=True, errors=None)


class Mutation(ObjectType):
    create_comment_category = CreateCommentCategory.Field()
