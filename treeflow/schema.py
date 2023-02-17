
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.directives import SchemaDirectiveExtension

from treeflow.corpus.schemas import bibliography, comment, corpus, dependency, feature, section_type, section, source, text, token, user
from treeflow.dict.schemas import lemma, meaning
from treeflow.images.schemas import image
from treeflow.dict.types import language
from typing import List, Optional

from strawberry.django import auth
from treeflow.corpus.types.user import User


@gql.type
class Query(
    bibliography.Query,
    comment.Query,
    corpus.Query,
    dependency.Query,
    image.Query,
    feature.Query,
    section_type.Query,
    section.Query,
    source.Query,
    text.Query,
    token.Query,
    user.Query,
    lemma.Query,
    meaning.Query
):

    me: User = auth.current_user()
    node: Optional[gql.Node] = gql.django.node()


@gql.type
class Mutation(
    bibliography.Mutation,
    comment.Mutation,
    dependency.Mutation,
    image.Mutation,
    feature.Mutation,
    section_type.Mutation,
    section.Mutation,
    source.Mutation,
    text.Mutation,
    token.Mutation,
    lemma.Mutation,
    meaning.Mutation
):
    login: User = auth.login()
    logout = auth.logout()
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[
                           DjangoOptimizerExtension, SchemaDirectiveExtension])
