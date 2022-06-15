from graphene import Enum, ObjectType, Field
from graphql_jwt.decorators import login_required


class CommentCategories(Enum):
    C = 'C'
    L = 'L'
    S = 'S'
    M = 'M'
    X = 'X'


# Query
class Query(ObjectType):
    category = Field(CommentCategories, description='Categories for classifying comments')

    @login_required
    def resolve_category(root, info, category):
        return category
