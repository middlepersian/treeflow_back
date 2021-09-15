import uuid as uuid_lib
from django.db import models


class SigleID(models.TextChoices):
    AM = "AM", "AM"
    AOD = "AOD", "AŌD"
    Aog = "Aog", "Aog"
    ASS = "ASS", "ASS"
    AWM = "AWM", "AWM"
    AWN = "AWN", "AWN"
    AZ = "AZ", "AZ"
    CHP = "CHP", "CHP"
    DA = "DA", "DA"
    Dd = "Dd", "Dd"
    Dk3 = "Dk3", "Dk3"
    Dk4 = "Dk4", "Dk4"
    Dk5 = "Dk5", "Dk5"
    Dk6 = "Dk6", "Dk6"
    Dk7 = "Dk7", "Dk7"
    Dk8 = "Dk8", "Dk8"
    Dk9 = "Dk9", "Dk9"
    DkC = "DkC", "DkC"
    DMX = "DMX", "DMX"
    ENN = "ENN", "ENN"
    GA = "GA", "GA"
    GBd = "GBd", "GBd"
    Her = "Her", "Hēr"
    HKR = "HKR", "HKR"
    HN = "HN", "HN"
    IndBd = "IndBd", "IndBd"
    KAP = "KAP", "KAP"
    MFRH = "MFRH", "MFRH"
    MHD = "MHD", "MHD"
    MK_Andarz = "MK_Andarz", "MK-Andarz"
    MYFr = "MYFr", "MYFr"
    N = "N", "N"
    NM = "NM", "NM"
    OHD = "OHD", "OHD"
    P = "P", "P"
    PahlRivDd = "PahlRivDd", "PahlRivDd"
    PT = "PT", "PT"
    PV = "PV", "PV"
    PY = "PY", "PY"
    RAF = "RAF", "RAF"
    REA = "REA", "RĒA"
    SGW = "SGW", "ŠGW"
    SiE = "SiE", "ŠiĒ"
    SnS = "SnS", "ŠnŠ"
    Vr = "Vr", "Vr"
    Vyt = "Vyt", "Vyt"
    WCNA = "WCNA", "WCNA"
    WD = "WD", "WD"
    WDWM = "WDWM", "WDWM"
    WZ = "WZ", "WZ"
    XD = "XD", "X&D"
    XAv = "XAv", "XAv"
    ZFJ = "ZFJ", "ZFJ"
    ZWY = "ZWY", "ZWY"


class Genre(models.TextChoices):
    ZAN = 'ZAN', "Zand"
    PTE = 'PTE', "PT-epitomes"
    PTR = 'PTR', "PT-reworking"
    TEO = "TEO", "theological"
    AUT = 'AUT',  "authorial-th"
    JUR = 'JUR', "jur"
    AND = 'AND', "andarz"
    NAR = 'NAR',  "narrative"


class TextSigle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid_lib.uuid4, editable=False)
    sigle = models.CharField(max_length=10, unique=True, choices=SigleID.choices)
    genre = models.CharField(max_length=3, unique=True, choices=Genre.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="valid_sigle",
                check=models.Q(sigle__in=SigleID.values),
            ),
            models.CheckConstraint(
                name="valid_genre",
                check=models.Q(genre__in=Genre.values),
            ),
            models.UniqueConstraint(
                fields=['sigle', 'genre'], name='sigle_genre'
            )
        ]
