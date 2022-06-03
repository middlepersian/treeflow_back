from graphene import Enum, ObjectType, Field


class Language(Enum):
    akk = 'akk'
    ara = 'ara'
    arc = 'arc'
    ave = 'ave'
    eng = 'eng'
    deu = 'deu'
    guj = 'guj'
    fra = 'fra'
    grc = 'grc'
    ita = 'ita'
    pal = 'pal'
    san = 'san'
    spa = 'spa'
    prp = 'prp'
    xpr = 'xpr'

    @property
    def description(self):
        return self.value


# Query
class Query(ObjectType):
    language = Field(Language, description='Language in ISO 639-3 format')

    def resolve_language(root, info, language):
        return language
