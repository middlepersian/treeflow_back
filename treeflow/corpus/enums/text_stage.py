from enum import StrEnum


class TextStage(StrEnum):
    raw = "Raw"
    preannotated = "Preannotated"
    prereview = "Pre-Reviewed"
    inprogress = "In Progress"
    annotated = "Annotated"
    reviewed = "Reviewed"