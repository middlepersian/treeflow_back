import strawberry
from asgiref.sync import sync_to_async
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List
from mpcd.corpus import models
from django.contrib.auth import get_user_model
from strawberry_django_plus.optimizer import DjangoOptimizerExtension


import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


@gql.django.type(get_user_model())
class User:
    id: gql.auto
    name: gql.auto
    is_superuser: gql.auto
    is_staff: gql.auto
    email: gql.auto


@gql.django.type(models.Comment)
class Comment:
    id: gql.auto
    user: 'User'
    text: gql.auto
    created_at: gql.auto
    updated_at: gql.auto


@gql.django.input(models.Comment)
class CommentInput:
    text: gql.auto


@gql.django.partial(models.Comment)
class CommentInputPartial(gql.NodeInput):
    text: gql.auto


@gql.type
class Query:
    comments: List[Comment] = gql.django.field()
    #logger.error("COMMENTS: {}".format(comments))


@gql.type
class Mutation:
    create_model: Comment = gql.django.create_mutation(CommentInput)
    update_model: Comment = gql.django.update_mutation(CommentInputPartial)
    delete_model: Comment = gql.django.delete_mutation(gql.NodeInput)


schema = strawberry.Schema(query=Query, extensions=[DjangoOptimizerExtension])