
import graphene
import graphql_jwt
import mpcd.corpus.schemas
import mpcd.dict.schemas


class Query(
        # Corpus Queries
        mpcd.corpus.schemas.author.Query,
        mpcd.corpus.schemas.bibliography.Query,
        mpcd.corpus.schemas.codex.Query,
        mpcd.corpus.schemas.codex_part.Query,
        mpcd.corpus.schemas.comment_category_enum.Query,
        mpcd.corpus.schemas.comment_category.Query,
        mpcd.corpus.schemas.corpus.Query,
        mpcd.corpus.schemas.dependency.Query,
        mpcd.corpus.schemas.dependency_enum.Query,
        mpcd.corpus.schemas.edition.Query,
        mpcd.corpus.schemas.facsimile.Query,
        mpcd.corpus.schemas.folio.Query,
        mpcd.corpus.schemas.line.Query,
        mpcd.corpus.schemas.morphological_annotation.Query,
        mpcd.corpus.schemas.morphological_annotation_enums.Query,
        mpcd.corpus.schemas.pos_enum.Query,
        mpcd.corpus.schemas.resource.Query,
        mpcd.corpus.schemas.section_type.Query,
        mpcd.corpus.schemas.stage_enum.Query,
        mpcd.corpus.schemas.text_sigle.Query,
        mpcd.corpus.schemas.text_sigle_enum.Query,
        mpcd.corpus.schemas.text.Query,
        mpcd.corpus.schemas.token.Query,
        mpcd.corpus.schemas.section.Query,
        mpcd.corpus.schemas.sentence.Query,
        # Dict Queries
        mpcd.dict.schemas.definition.Query,
        mpcd.dict.schemas.dictionary.Query,
        mpcd.dict.schemas.lemma.Query,
        mpcd.dict.schemas.language_enum.Query,
        mpcd.dict.schemas.meaning.Query,
        mpcd.dict.schemas.reference.Query,
        mpcd.dict.schemas.semantic.Query,
        mpcd.dict.schemas.term_tech.Query,
        graphene.ObjectType):
    pass


class Mutation(
        # Corpus Mutations
        mpcd.corpus.schemas.author.Mutation,
        mpcd.corpus.schemas.bibliography.Mutation,
        mpcd.corpus.schemas.codex.Mutation,
        mpcd.corpus.schemas.codex_part.Mutation,
        mpcd.corpus.schemas.corpus.Mutation,
        mpcd.corpus.schemas.dependency.Mutation,
        mpcd.corpus.schemas.edition.Mutation,
        mpcd.corpus.schemas.facsimile.Mutation,
        mpcd.corpus.schemas.folio.Mutation,
        mpcd.corpus.schemas.line.Mutation,
        mpcd.corpus.schemas.morphological_annotation.Mutation,
        mpcd.corpus.schemas.resource.Mutation,
        mpcd.corpus.schemas.sentence.Mutation,
        mpcd.corpus.schemas.section.Mutation,
        mpcd.corpus.schemas.section_type.Mutation,
        mpcd.corpus.schemas.text_sigle.Mutation,
        mpcd.corpus.schemas.text.Mutation,
        mpcd.corpus.schemas.token.Mutation,
        # Dict Mutations
        mpcd.dict.schemas.definition.Mutation,
        mpcd.dict.schemas.dictionary.Mutation,
        mpcd.dict.schemas.lemma.Mutation,
        mpcd.dict.schemas.meaning.Mutation,
        mpcd.dict.schemas.reference.Mutation,
        mpcd.dict.schemas.semantic.Mutation,
        mpcd.dict.schemas.term_tech.Mutation,
        graphene.ObjectType):

    # https://django-graphql-jwt.domake.io/relay.html
    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()

    # Long running refresh tokens
    revoke_token = graphql_jwt.relay.Revoke.Field()
    delete_refresh_token_cookie = \
        graphql_jwt.relay.DeleteRefreshTokenCookie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
