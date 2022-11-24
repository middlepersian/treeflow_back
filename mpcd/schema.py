
import strawberry
from strawberry_django_plus import gql
import strawberry_django_jwt.mutations as jwt_mutations
from strawberry_django_jwt.middleware import AsyncJSONWebTokenMiddleware
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.schemas import bibliography, codex_part, comment, corpus, dependency, facsimile, folio, line, morphological_annotation, section_type, section, sentence, source, text_sigle, text, token_comment, token, user
from mpcd.dict.schemas import lemma, meaning
from mpcd.dict.types import language
from typing import List


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
    token.Query,
    user.Query,
    lemma.Query,
    meaning.Query
):

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
    pass
    # https://django-graphql-jwt.domake.io/relay.html
    # token_auth = jwt_mutations.ObtainJSONWebTokenAsync.obtain
    # verify_token = jwt_mutations.VerifyAsync.verify
    # refresh_token = jwt_mutations.RefreshAsync.refresh
    # delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookieAsync.delete_cookie

    # Long running refresh tokens
    # revoke_token = graphql_jwt.relay.Revoke.Field()
    # delete_refresh_token_cookie = \
    #    graphql_jwt.relay.DeleteRefreshTokenCookie.Field()

    # schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[AsyncJSONWebTokenMiddleware,  DjangoOptimizerExtension])
schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
