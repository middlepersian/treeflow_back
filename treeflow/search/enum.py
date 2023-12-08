from enum import StrEnum
import strawberry


@strawberry.enum
class SearchType(StrEnum):
    SIMPLE = "simple"
    BY_POSITION = "by_position"
