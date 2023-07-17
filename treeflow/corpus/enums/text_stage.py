from enum import StrEnum
import strawberry

@strawberry.enum
class TextStage(StrEnum):
    untouched = "untouched"
    in_progress = "inprogress"
    finished = "finished"
    unset = ""