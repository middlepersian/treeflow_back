
import strawberry
from strawberry_django_plus import gql
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.schemas import bibliography, codex_part, comment, corpus, dependency, facsimile, folio, line, morphological_annotation, section_type, section, sentence, source, text_sigle, text, token_comment, token, user
from mpcd.dict.schemas import lemma, meaning
from mpcd.dict.types import language
from typing import List, Union

from gqlauth.user.queries import UserQueries
from gqlauth.core.field_ import field
from gqlauth.core.types_ import GQLAuthError
from gqlauth.core.directives import TokenRequired
from gqlauth.user import relay as mutations



@strawberry.type
class MyAuthorizedQueries(UserQueries, token.Query):
    # add your queries that require authorization here.
    pass


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
    token_comment.Query,
    user.Query,
    lemma.Query,
    meaning.Query
):
    @field(directives=[TokenRequired()])
    def auth_entry(self) -> Union[GQLAuthError, MyAuthorizedQueries]:
        return MyAuthorizedQueries()

    @gql.field
    def languages(self, info) -> List[language.Language]:
        return language.Language
    pass


@strawberry.type
class AuthMutation:
    # include here your mutations that interact with a user object from a token.

    verify_token = mutations.VerifyToken.field
    refresh_token = mutations.RefreshToken.field

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
    @field(directives=[TokenRequired()])
    def auth_entry(self) -> Union[AuthMutation, GQLAuthError]:
        return AuthOutput(node=AuthMutation())


    token_auth = mutations.ObtainJSONWebToken.field


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
