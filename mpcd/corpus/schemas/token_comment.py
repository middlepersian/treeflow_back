from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from mpcd.corpus.models import TokenComment
from mpcd.corpus.schemas.comment_category_enum import CommentCategories

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TokenCommentNode(DjangoObjectType):
    class Meta:
        model = TokenComment
        filter_fields = {
            'user__id': ['exact'],
            'uncertain__id': ['exact'],
            'to_discuss__id': ['exact'],
            'new_suggestion__id': ['exact'],
            'text': ['icontains']
        }
        interfaces = (relay.Node, )


class TokenCommentInput(InputObjectType):
    user = ID
    uncertain = List(ID, required=True)
    to_discuss = List(ID, required=True)
    new_suggestion = List(ID, required=True)
    text = String(required=True)


class Query(ObjectType):
    comment = relay.Node.Field(TokenCommentNode)
    comments = DjangoFilterConnectionField(TokenCommentNode)

    @login_required
    def resolve_comments(self, info, **kwargs):
        qs = TokenComment.objects.all()
        return gql_optimizer.query(qs, info)

    @login_required
    def resolve_comment(self, info, id):
        id = from_global_id(id)[1]
        return TokenComment.objects.get(pk=id)

# Mutations


class CreateTokenComment(relay.ClientIDMutation):
    class Input:
        user = ID
        uncertain = List(ID, required=True)
        to_discuss = List(ID, required=True)
        new_suggestion = List(ID, required=True)
        text = String(required=True)

    comment = Field(TokenComment)
    errors = List(String)
    success = Boolean()

    @login_required
    def mutate_and_get_payload(root, info, **input):
        comment_obj, comment_created = TokenComment.objects.create(user=input.get('user'), text=input.get('text'))
        for unc in input.get('uncertain'):
            if CommentCategory.objects.filter(pk=from_global_id(unc)[1]).exists():
                comment_obj.uncertain.add(CommentCategory.objects.get(pk=from_global_id(unc)[1]))
        for td in input.get('to_discuss'):
            if CommentCategory.objects.filter(pk=from_global_id(td)[1]).exists():
                comment_obj.to_discuss.add(CommentCategory.objects.get(pk=from_global_id(td)[1]))
        for ns in input.get('new_suggestion'):
            if CommentCategory.objects.filter(pk=from_global_id(ns)[1]).exists():
                comment_obj.new_suggestion.add(CommentCategory.objects.get(pk=from_global_id(ns)[1]))

        comment_obj.save()
        return cls(comment=comment_obj, success=True, errors=None)


class UpdateTokenComment(relay.ClientIDMutation):

    class Input:
        id = ID
        user = ID
        uncertain = List(ID, required=True)
        to_discuss = List(ID, required=True)
        new_suggestion = List(ID, required=True)
        text = String(required=True)

    comment = Field(CommentNode)
    errors = List(String)
    success = Boolean()

    @login_required
    def mutate_and_get_payload(root, info, **input):
        if TokenComment.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            comment_obj = TokenComment.objects.get(pk=from_global_id(input.get('id'))[1])
            comment_obj.user = user
            comment_obj.text = text
            for unc in input.get('uncertain'):
                if CommentCategory.objects.filter(pk=from_global_id(unc)[1]).exists():
                    comment_obj.uncertain.add(CommentCategory.objects.get(pk=from_global_id(unc)[1]))
            for td in input.get('to_discuss'):
                if CommentCategory.objects.filter(pk=from_global_id(td)[1]).exists():
                    comment_obj.to_discuss.add(CommentCategory.objects.get(pk=from_global_id(td)[1]))
            for ns in input.get('new_suggestion'):
                if CommentCategory.objects.filter(pk=from_global_id(ns)[1]).exists():
                    comment_obj.new_suggestion.add(CommentCategory.objects.get(pk=from_global_id(ns)[1]))
            comment_obj.save()
            return cls(comment=comment_obj, success=True, errors=None)
        else:
            return cls(comment=None, success=False, errors=['Comment ID not found'])


class DeleteTokenComment(relay.ClientIDMutation):

    class Input:
        id = ID

    comment = Field(TokenCommentNode)
    errors = List(String)
    success = Boolean()

    @login_required
    def mutate_and_get_payload(root, info, id):
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
