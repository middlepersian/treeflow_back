from enum import StrEnum
import strawberry

@strawberry.enum

class CommentCategories(StrEnum):
    C = 'C' #'transcription'
    L = 'L' #'transliteration'
    S = 'S' #'semantics'
    M = 'M' #'morphology'
    P = 'P' #'reading_of_a_passage'
    X = 'X' #'syntax'

    