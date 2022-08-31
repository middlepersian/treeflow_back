
from strawberry_django_plus import gql
import strawberry_django_jwt.mutations as jwt_mutations
from strawberry_django_jwt.middleware import AsyncJSONWebTokenMiddleware


@gql.type
class Query():
    @gql.field
    async def hello(self) -> str:
        return "Hello World"


@gql.type
class Mutation:
    # https://django-graphql-jwt.domake.io/relay.html
    token_auth = jwt_mutations.ObtainJSONWebTokenAsync.obtain
    verify_token = jwt_mutations.VerifyAsync.verify
    refresh_token = jwt_mutations.RefreshAsync.refresh
    delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookieAsync.delete_cookie

    # Long running refresh tokens
    #revoke_token = graphql_jwt.relay.Revoke.Field()
    # delete_refresh_token_cookie = \
    #    graphql_jwt.relay.DeleteRefreshTokenCookie.Field()


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[AsyncJSONWebTokenMiddleware])
