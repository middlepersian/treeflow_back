from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from mpcd.corpus.models import Comment

@gql.django.type(Comment)
class AssetNode(relay.Node):
    text: gql.auto
    user: UserNode


@gql.django.partial(Comment)
class UpdateCommentInput(gql.NodeInput):
    text: gql.auto


@gql.type
class ModelMutation:

    @gql.mutation
    def update_comment(self, info: Info, input: UpdateCommentInput) -> ModelNode:
        data = vars(input)
        node_id: relay.GlobalID = data.pop('id')
        comment: Asset = node_id.resolve_node(info, ensure_type=Comment)

        if comment.owner != info.context.request.user:
            raise PermissionError("You can only modify objects you own.")

        return resolvers.update(info, asset, resolvers.parse_input(info, data))
