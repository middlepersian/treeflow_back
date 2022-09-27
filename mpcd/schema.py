
import strawberry
from strawberry_django_plus import gql
import strawberry_django_jwt.mutations as jwt_mutations
from strawberry_django_jwt.middleware import AsyncJSONWebTokenMiddleware
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from mpcd.corpus.schemas import comment, token


@gql.type
class Query(comment.Query, token.Query):
    pass


@gql.type
class Mutation():
    # https://django-graphql-jwt.domake.io/relay.html
    token_auth = jwt_mutations.ObtainJSONWebTokenAsync.obtain
    verify_token = jwt_mutations.VerifyAsync.verify
    refresh_token = jwt_mutations.RefreshAsync.refresh
    delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookieAsync.delete_cookie

    # Long running refresh tokens
    #revoke_token = graphql_jwt.relay.Revoke.Field()
    # delete_refresh_token_cookie = \
    #    graphql_jwt.relay.DeleteRefreshTokenCookie.Field()


#schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[AsyncJSONWebTokenMiddleware,  DjangoOptimizerExtension])
schema = strawberry.Schema(query=Query)
