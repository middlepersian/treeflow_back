from enum import StrEnum
import strawberry

@strawberry.enum

class CommentCategories(StrEnum):
    transcription = 'C' 
    transliteration = 'L' 
    semantics = 'S' 
    morphology = 'M' 
    reading_of_a_passage = 'P' 
    syntax = 'X' 

    