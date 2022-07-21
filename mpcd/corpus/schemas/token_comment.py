from mpcd.corpus.schemas.comment_category_enum import CommentCategories
from mpcd.corpus.models import TokenComment
from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from django.contrib.auth import get_user_model
User = get_user_model()


class TokenCommentNode(DjangoObjectType):

    class Meta:
        model = TokenComment
        filter_fields = {
            'user__id': ['exact'],
            'text': ['icontains']
        }
        fields = "__all__"
        interfaces = (relay.Node, )


class TokenCommentInput(InputObjectType):
    user = ID(required=False)
    uncertain = List(ID, required=True)
    to_discuss = List(ID, required=True)
    new_suggestion = List(ID, required=True)
    text = String(required=True)


class Query(ObjectType):
    token_comment = relay.Node.Field(TokenCommentNode)
    all_token_comments = DjangoFilterConnectionField(TokenCommentNode)

    @login_required
    def resolve_all_token_comments(self, info, **kwargs):
        qs = TokenComment.objects.all()
        return gql_optimizer.query(qs, info)

    @login_required
    def resolve_token_comment(self, info, id):
        id = from_global_id(id)[1]
        return TokenComment.objects.get(pk=id)

# Mutations


class CreateTokenComment(relay.ClientIDMutation):
    class Input:
        user = ID(required=False)
        uncertain = List(String, required=True)
        to_discuss = List(String, required=True)
        new_suggestion = List(String, required=True)
        text = String(required=False)

    comment = Field(TokenCommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        comment_obj = TokenComment.objects.create(text=input.get('text',  None))
        if input.get('user', None):
            user_id = from_global_id(input.get('user'))[1]
            if User.objects.filter(pk=user_id).exists():
                comment_obj.user = User.objects.get(pk=user_id)

        if input.get('uncertain'):
            comment_obj.uncertain = input.get('uncertain')
        if input.get('to_discuss'):
            comment_obj.to_discuss = input.get('to_discuss')
        if input.get('new_suggestion'):
            comment_obj.new_suggestion = input.get('new_suggestion')

        comment_obj.save()
        return cls(comment=comment_obj, success=True, errors=None)


class UpdateTokenComment(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)
        user = ID(required=False)
        uncertain = List(String, required=True)
        to_discuss = List(String, required=True)
        new_suggestion = List(String, required=True)
        text = String(required=True)

    comment = Field(TokenCommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if TokenComment.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            comment_obj = TokenComment.objects.get(pk=from_global_id(input.get('id'))[1])
            comment_obj.user = user
            comment_obj.text = text

            # Update the comment categories
            if input.get('uncertain'):
                comment_obj.uncertain = input.get('uncertain')
            if input.get('to_discuss'):
                comment_obj.to_discuss = input.get('to_discuss')
            if input.get('new_suggestion'):
                comment_obj.new_suggestion = input.get('new_suggestion')

            comment_obj.save()
            return cls(comment=comment_obj, success=True, errors=None)
        else:
            return cls(comment=None, success=False, errors=['Comment ID not found'])


class DeleteTokenComment(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)

    comment = Field(TokenCommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if TokenComment.objects.filter(pk=from_global_id(id)[1]).exists():
            comment_obj = TokenComment.objects.get(pk=from_global_id(id)[1])
            comment_obj.delete()
            return cls(comment=comment_obj, success=True, errors=None)
        else:
            return cls(comment=None, success=False, errors=['TokenComment ID not found'])


class Mutation:
    create_token_comment = CreateTokenComment.Field()
    update_token_comment = UpdateTokenComment.Field()
    delete_token_comment = DeleteTokenComment.Field()
