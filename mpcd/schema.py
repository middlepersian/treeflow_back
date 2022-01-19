
import graphene
import mpcd.corpus.schema
#import mpcd.dict.schema


class Query(mpcd.corpus.schema.Query, graphene.ObjectType):
    pass


#class Mutation(mpcd.corpus.Mutation, graphene.ObjectType):
#    pass


schema = graphene.Schema(query=Query)
