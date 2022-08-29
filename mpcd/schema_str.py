
from strawberry_django_plus import gql
import strawberry_django_jwt.mutations as jwt_mutations
import mpcd.corpus.schemas
import mpcd.dict.schemas


@gql.type
class Query():
    pass


@gql.type
class Mutation():
    # https://django-graphql-jwt.domake.io/relay.html
    token_auth = jwt_mutations.ObtainJSONWebToken.obtain
    verify_token = jwt_mutations.Verify.verify
    refresh_token = jwt_mutations.Refresh.refresh
    delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookie.delete_cookie

    # Long running refresh tokens
    #revoke_token = graphql_jwt.relay.Revoke.Field()
    # delete_refresh_token_cookie = \
    #    graphql_jwt.relay.DeleteRefreshTokenCookie.Field()


schema = strawberry.Schema(query=Query, mutation=Mutation)
