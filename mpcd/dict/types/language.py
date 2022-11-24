from strawberry_django_plus import gql
from enum import Enum
import strawberry


@strawberry.enum
class Language(Enum):
    pal = "pal"
    eng = "eng"
    deu = "deu"
    ita = "ita"


