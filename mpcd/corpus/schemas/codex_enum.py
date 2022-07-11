from graphene import Enum, ObjectType, Field


class Codices(Enum):

    DH6 = 'DH6'
    B = 'B'
    BK = 'BK'
    IOL = 'IOL'
    J58 = 'J58'
    K20 = 'K20'
    K20b = 'K20b'
    K27 = 'K27'
    K35 = 'K35'
    K43a = 'K43a'
    K43b = 'K43b'
    K26 = 'K26'
    MJ = 'MJ'
    msMHD = 'msMHD'
    M51 = 'M51'
    M51b = 'M51b'
    P = 'P'
    Pt4 = 'Pt4'
    TD1 = 'TD1'
    TD2 = 'TD2'
    TD4a = 'TD4a'


# Query
class Query(ObjectType):
    codex = Field(Codices, description='List of Codex Sigles')


    def resolve_codex(root, info, codex):
        return codex
