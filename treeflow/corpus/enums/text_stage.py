from enum import StrEnum


class TextStage(StrEnum):
    untouched = "untouched"
    in_progress = "inprogress"
    finished = "finished"
    unset = ""