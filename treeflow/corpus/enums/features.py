import strawberry

@strawberry.type
class UPOS_Feature:
    upos: str
    feat: str
    values: List[str]

from typing import List

data = [
    ("ADV", "Deixis", ["Prox","Remt"]),
    ("DET", "Definite", ["Ind","Spec"]),
    ("DET", "PronType", ["Dem","Ind","Tot","Int"]),
    ("DET", "Deixis", ["Prox","Remt"]),
    ("PUNCT", "PunctType", ["Semi","Dash","Excl","Quot"]),
    ("PUNCT", "PunctSide", ["Ini","Fin"]),
    ("SCONJ", "PronType", ["Rel"]),
    ("NUM", "NumType", ["Card","Fract","Sets"]),
    ("PART", "PartType", ["Mod","Neg","Emp","Vbp"]),
    ("PRON", "PronType", ["Prs","Dem","Int","Rel","Tot","Ing","Neg","Exc"]),
    ("PRON", "Person", ["1","2","3"]),
    ("PRON", "Number", ["Sing","Plur"]),
    ("PRON", "Case", ["Nom","Acc"]),
    ("PRON", "Polite", ["Inform","Form","Elev","Humb"]),
    ("PRON", "Deixis", ["Prox","Remt"]),
    ("NOUN", "Number", ["Sing","Plur"]),
    ("NOUN", "Polite", ["Inform","Form","Elev","Humb"]),
    ("NOUN", "Animacy", ["Hum","Nhum","Inan"]),
    ("NOUN", "Gender", ["Fem","Masc"]),
    ("NOUN", "Case", ["Nom","Acc"]),
    ("NOUN", "Subcat", ["Tran"]),
    ("NOUN", "VerbForm", ["Inf","Part","Vnoun"]),
    ("PROPN", "NameType", ["Giv","Pat","Geo","Oth"]),
    ("PROPN", "Transc", ["Yes"]),
    ("SYM", "Text", []),
    ("AUX", "VerbType", ["Cop","Quasi","Light","Mod"]),
    ("AUX", "Subcat", ["Tran","Intr"]),
    ("AUX", "Tense", ["Pres","Past"]),
    ("AUX", "Mood", ["Ind","Sub","Opt","Imp","Nec"]),
    ("AUX", "Person", ["1","2","3"]),
    ("AUX", "Number", ["Sing","Plur"]),
    ("AUX", "VerbForm", ["Fin","Inf","Conv"]),
    ("AUX", "Polarity", ["Neg"])
]

