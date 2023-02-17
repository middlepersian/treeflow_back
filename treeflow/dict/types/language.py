from strawberry_django_plus import gql
from enum import StrEnum
import strawberry


@strawberry.enum
class Language(StrEnum):
    pal = "pal"
    eng = "eng"
    deu = "deu"
    ita = "ita"
    esp = "spa"
    fra = "fra"