from enum import StrEnum
import strawberry



@strawberry.enum
class Language(StrEnum):
    Middle_Persian = "pal"
    Imperial_Aramaic = "arc"
    Avestan = "ave"
    Ancient_Greek = "grc"
    Parthian = "xpr"
    Parsi = "prp"
    Arabic = "ara"
    Gujarati = "guj"
    Sanskrit = "san"
    English = "eng"
    French = "fra"
    German = "deu"
    Italian = "ita"
    Spanish = "spa"
