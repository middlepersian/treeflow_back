from graphene import Enum, ObjectType, Field


class Language(Enum):
    Akkadian = 'akk'
    Arabic = 'ara'
    Imperial_Aramaic = 'arc'
    Avestan = 'ave'
    English = 'eng'
    German = 'deu'
    French = 'guj'
    French = 'fra'
    Ancient_Greek = 'grc'
    Italian = 'ita'
    Pahlavi = 'pal'
    Sanskrit = 'san'
    Spanish = 'spa'
    Parsi = 'prp'
    Parthian = 'xpr'

    @property
    def description(self):
        return self.value


# Query
class Query(ObjectType):
    language = Field(Language)

    def resolve_language(root, info, language):
        return language
