from enum import StrEnum
import strawberry

@strawberry.enum

class TermTech(StrEnum):
    astronomy = "astr"
    botany = "bot"
    economics = "econom"
    legal = "legal"
    measurement = "measure"
    medicine = "med"
    philosophy = "philos"
    politics = "pol"
    purity = "purity"
    ritual = "ritual"
    theology = "theol"
    zoology = "zool"