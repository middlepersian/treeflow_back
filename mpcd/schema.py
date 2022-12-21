
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.directives import SchemaDirectiveExtension

from mpcd.corpus.schemas import bibliography, codex_part, comment, corpus, dependency, facsimile, folio, line, morphological_annotation, section_type, section, sentence, source, text_sigle, text, token_comment, token, user
from mpcd.dict.schemas import lemma, meaning
from mpcd.dict.types import language
from typing import List

from strawberry.django import auth
from mpcd.corpus.types.user import User


@gql.type
class Query(
    bibliography.Query,
    codex_part.Query,
    comment.Query,
    corpus.Query,
    dependency.Query,
    facsimile.Query,
    folio.Query,
    line.Query,
    morphological_annotation.Query,
    section_type.Query,
    section.Query,
    sentence.Query,
    source.Query,
    text_sigle.Query,
    text.Query,
    token.Query,
    token_comment.Query,
    user.Query,
    lemma.Query,
    meaning.Query
):

    me: User = auth.current_user()
    node = relay.node()


    @gql.field
    def languages(self, info) -> List[language.Language]:
        return language.Language
    pass


@gql.type
class Mutation(
    bibliography.Mutation,
    codex_part.Mutation,
    comment.Mutation,
    dependency.Mutation,
    facsimile.Mutation,
    folio.Mutation,
    line.Mutation,
    morphological_annotation.Mutation,
    section_type.Mutation,
    section.Mutation,
    sentence.Mutation,
    source.Mutation,
    text_sigle.Mutation,
    text.Mutation,
    token_comment.Mutation,
    token.Mutation,
    lemma.Mutation,
    meaning.Mutation
):
    login: User = auth.login()
    logout = auth.logout()
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[
                           DjangoOptimizerExtension, SchemaDirectiveExtension])
