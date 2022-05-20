from graphene import Enum


class ADJ(Enum):
    NumType = 'NumType'
    Poss = "Poss"
    Number = "Number"
    Case = "Case"
    VerbForm = "VerbForm"
    Voice = "Voice"
    Polarity = "Polarity"

    @property
    def description(self):
        return self.value


class ADJNumType(Enum):
    Ord = 'Ord'
    Mult = 'Ord'

    @property
    def description(self):
        return self.value


class ADJPoss(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class ADJNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value


class ADJCase(Enum):
    Nom = 'Nom'
    Acc = 'Acc'

    @property
    def description(self):
        return self.value


class ADJDegree(Enum):
    Cmp = 'Cmp'
    Pos = 'Pos'
    Sup = 'Sup'

    @property
    def description(self):
        return self.value


class ADJVerbForm(Enum):
    Part = 'Part'

    @property
    def description(self):
        return self.value


class ADJTense(Enum):
    Past = 'Past'
    Pres = 'Pres'

    @property
    def description(self):
        return self.value


class ADJVoice(Enum):
    Act = 'Act'
    Pass = 'Pass'
    Cau = 'Cau'

    @property
    def description(self):
        return self.value


class ADJPolarity(Enum):
    Neg = 'Neg'

    @property
    def description(self):
        return self.value
