import pytest
from django.contrib.auth import get_user_model
from typing import List
import strawberry_django
from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
import asyncio

from mpcd.corpus import models
from . import utils


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


@gql.type
class Mutation:
    create_model: Comment = gql.django.create_mutation(CommentInput)
    update_model: Comment = gql.django.update_mutation(CommentInputPartial)
    delete_model: Comment = gql.django.delete_mutation(gql.NodeInput)

'''
def test_async():
    def is_async() -> bool:
        # django uses the same method to detect async operation
        # https://github.com/django/django/blob/bb076476cf560b988f8d80dbbc4a3c85df54b1b9/django/utils/asyncio.py
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return False
        else:
            return True

    assert is_async()
'''    


def test_query(db):
    print(utils.generate_query(Query))
    assert True
