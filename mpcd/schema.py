
import graphene
import mpcd.corpus.schemas

#import mpcd.dict.schema


class Query(
        mpcd.corpus.schemas.author.Query,
        mpcd.corpus.schemas.bibliography.Query,
        mpcd.corpus.schemas.codex.Query,
        mpcd.corpus.schemas.corpus.Query,
        mpcd.corpus.schemas.dependency.Query,
        mpcd.corpus.schemas.feature.Query,
        mpcd.corpus.schemas.feature_value.Query,
        mpcd.corpus.schemas.folio.Query,
        mpcd.corpus.schemas.line.Query,
        mpcd.corpus.schemas.morphological_annotation.Query,
        mpcd.corpus.schemas.pos.Query,
        mpcd.corpus.schemas.resource.Query,
        mpcd.corpus.schemas.text_sigle.Query,
       # mpcd.corpus.schemas.token.Query,
        graphene.ObjectType):
    pass


class Mutation(mpcd.corpus.schemas.author.Mutation,
               mpcd.corpus.schemas.bibliography.Mutation,
               mpcd.corpus.schemas.codex.Mutation,
               mpcd.corpus.schemas.corpus.Mutation,
               mpcd.corpus.schemas.dependency.Mutation,
               mpcd.corpus.schemas.feature.Mutation,
               mpcd.corpus.schemas.feature_value.Mutation,
               mpcd.corpus.schemas.folio.Mutation,
               mpcd.corpus.schemas.line.Mutation,
               mpcd.corpus.schemas.morphological_annotation.Mutation,
               mpcd.corpus.schemas.pos.Mutation,
               mpcd.corpus.schemas.resource.Mutation,
               mpcd.corpus.schemas.text_sigle.Mutation,
            #   mpcd.corpus.schemas.token.Mutation,
               graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)