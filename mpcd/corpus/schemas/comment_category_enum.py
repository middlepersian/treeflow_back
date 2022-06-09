from graphene import Enum, ObjectType, Field
from graphql_jwt.decorators import login_required


class CommentCategories(Enum):
    transcription = 'C'
    transliteration = 'L'
    semantics = 'S'
    morphology = 'M'
    syntax = 'X'

    @property
    def description(self):
        return self.value


# Query
class Query(ObjectType):
    category = Field(CommentCategories, description='Categories for classifying comments')

    @login_required
    def resolve_category(root, info, category):
        return category
