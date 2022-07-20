from graphene import relay, ObjectType, Field, ID, Boolean, List, InputObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User
from mpcd.corpus.models import Comment


class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        filter_fields = {
            'user__id': ['exact'],
            'text': ['icontains']
        }
        interfaces = (relay.Node, )


class CommentInput(InputObjectType):
    user = ID(required=False)
    text = String(required=True)


class Query(ObjectType):
    comment = relay.Node.Field(CommentNode)
    all_comments = DjangoFilterConnectionField(CommentNode)

    @login_required
    def resolve_all_comments(self, info, **kwargs):
        qs = Comment.objects.all()
        return gql_optimizer.query(qs, info)

    @login_required
    def resolve_comment(self, info, id):
        id = from_global_id(id)[1]
        return Comment.objects.get(pk=id)

# Mutations


class CreateComment(relay.ClientIDMutation):
    class Input:
        user = ID(required=False)
        text = String(required=True)

    comment = Field(CommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        comment_obj = Comment.objects.create(text=input.get('text'))
        if input.get('user', None):
            user_id = from_global_id(input.get('user'))[1]
            if User.objects.filter(pk=user_id).exists():
                comment_obj.user = User.objects.get(pk=user_id)

        comment_obj.save()
        return cls(comment=comment_obj, success=True, errors=None)


class UpdateComment(relay.ClientIDMutation):

    class Input:
        id = ID(required=True)
        user = ID(required=True)
        text = String(required=True)

    comment = Field(CommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Comment.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            comment_obj = Comment.objects.get(pk=from_global_id(input.get('id'))[1])

            comment_obj.text = text

            if User.objects.filter(pk=from_global_id(input.get('user'))[1]).exists():
                comment_obj.user = User.objects.get(pk=from_global_id(input.get('user'))[1])

            comment_obj.save()
            return cls(comment=comment_obj, success=True, errors=None)
        else:
            return cls(comment=None, success=False, errors=['Comment ID not found'])


class DeleteComment(relay.ClientIDMutation):

    class Input:
        id = ID

    comment = Field(CommentNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if Comment.objects.filter(pk=from_global_id(id)[1]).exists():
            comment_obj = Comment.objects.get(pk=from_global_id(id)[1])
            comment_obj.delete()
            return cls(comment=comment_obj, success=True, errors=None)
        else:
            return cls(comment=None, success=False, errors=['Comment ID not found'])


class Mutation:
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
