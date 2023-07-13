from enum import StrEnum
import strawberry

@strawberry.enum
class DictStage(StrEnum):
    automatic = "automatic"
    manual = "manual"
    verified = "verified"
    unverified = "unverified"
    unset = ""