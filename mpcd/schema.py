
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.directives import SchemaDirectiveExtension

from mpcd.corpus.schemas import bibliography, comment, corpus, dependency, facsimile, folio, morphological_annotation, section_type, section, source, text_sigle, text, token, user
from mpcd.dict.schemas import lemma, meaning
from mpcd.dict.types import language
from typing import List, Optional

from strawberry.django import auth
from mpcd.corpus.types.user import User


@gql.type
class Query(
    bibliography.Query,
    comment.Query,
    corpus.Query,
    dependency.Query,
    facsimile.Query,
    folio.Query,
    morphological_annotation.Query,
    section_type.Query,
    section.Query,
    source.Query,
    text_sigle.Query,
    text.Query,
    token.Query,
    user.Query,
    lemma.Query,
    meaning.Query
):

    me: User = auth.current_user()
    node: Optional[gql.Node] = gql.django.node()

    @gql.field
    def languages(self, info) -> List[language.Language]:
        return language.Language
    pass


@gql.type
class Mutation(
    bibliography.Mutation,
    comment.Mutation,
    dependency.Mutation,
    facsimile.Mutation,
    folio.Mutation,
    morphological_annotation.Mutation,
    section_type.Mutation,
    section.Mutation,
    source.Mutation,
    text_sigle.Mutation,
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
