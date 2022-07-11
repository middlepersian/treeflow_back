
from graphene import Enum, ObjectType, Field


class SigleID(Enum):
    AM = "AM"
    AOD = "AOD"
    Aog = "Aog"
    ASS = "ASS"
    AWM = "AWM"
    AWN = "AWN"
    AZ = "AZ"
    CHP = "CHP"
    DA = "DA"
    Dd = "Dd"
    Dk3 = "Dk3"
    Dk4 = "Dk4"
    Dk5 = "Dk5"
    Dk6 = "Dk6"
    Dk7 = "Dk7"
    Dk8 = "Dk8"
    Dk9 = "Dk9"
    DkC = "DkC"
    DMX = "DMX"
    ENN = "ENN"
    GA = "GA"
    GBd = "GBd"
    Her = "Her"
    HKR = "HKR"
    HN = "HN"
    IndBd = "IndBd"
    KAP = "KAP"
    MFRH = "MFRH"
    MHD = "MHD"
    MK_Andarz = "MK_Andarz"
    MYFr = "MYFr"
    N = "N"
    NM = "NM"
    OHD = "OHD"
    P = "P"
    PahlRivDd = "PahlRivDd"
    PT = "PT"
    PV = "PV"
    PY = "PY"
    RAF = "RAF"
    REA = "REA"
    SGW = "SGW"
    SiE = "SiE"
    SnS = "SnS"
    Vr = "Vr"
    Vyt = "Vyt"
    WCNA = "WCNA"
    WD = "WD"
    WDWM = "WDWM"
    WZ = "WZ"
    XD = "XD"
    XAv = "XAv"
    ZFJ = "ZFJ"
    ZWY = "ZWY"


class Genre(Enum):
    zand = 'ZAN'
    PT_epitomes = 'PTE'
    PT_reworking = 'PTR'
    theological = 'TEO'
    authorial_th = 'AUT'
    juridical = 'JUR'
    andarz = 'AND'
    narrative = 'NAR'


# Query
class Query(ObjectType):
    sigle_id = Field(SigleID, description='List of Text Sigles')

    def resolve_sigle_ids(root, info, sigle_id):
        return sigle_id

    genre = Field(Genre, description='List of Genres')

    def resolve_genre(root, info, genre):
        return genre
