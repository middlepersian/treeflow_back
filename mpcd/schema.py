
import graphene
import mpcd.corpus.schemas.author
import mpcd.corpus.schemas.bibliography
#import mpcd.dict.schema


class Query(
        mpcd.corpus.schemas.author.Query,
        mpcd.corpus.schemas.bibliography.Query,
        graphene.ObjectType):
    pass


class Mutation(mpcd.corpus.schemas.author.Mutation,
               mpcd.corpus.schemas.bibliography.Mutation,
               graphene.ObjectType):

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
