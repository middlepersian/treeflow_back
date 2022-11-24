from strawberry_django_plus import gql
from enum import Enum

@gql.enum
class Language(Enum):
    Pahlavi = "pal"
    English = "eng"
    German = "ger"