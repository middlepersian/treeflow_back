from graphene import Enum, ObjectType, Field


class Stage(Enum):
    untouched = 'unt'
    in_progress = 'pro'
    finished = 'fin'


class Query(ObjectType):
    stage = Field(Stage, description="Text stage")

    def resolve_stage(root, info, stage):
        return stage
