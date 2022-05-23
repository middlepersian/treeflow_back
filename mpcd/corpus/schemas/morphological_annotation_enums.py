from tokenize import Number
from graphene import Enum


# Adjective features
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

# Adposition features


class ADP(Enum):
    Pos = 'Pos'

    @property
    def description(self):
        return self.value


class ADPPos(Enum):
    Pre = 'Pre'
    Post = 'Post'
    Circum = 'Circum'

    @property
    def description(self):
        return self.value


# Adverbial features

class ADV(Enum):
    PronType = 'PronType'
    NumType = 'NumType'
    Degree = 'Degree'
    VerbForm = 'VerbForm'
    Tense = 'Tense'
    Voice = 'Voice'
    Polarity = 'Polarity'

    @property
    def description(self):
        return self.value


class ADVProType(Enum):

    Dem = 'Dem'
    Ind = 'Ind'
    Int = 'Int'
    Neg = 'Neg'
    Rel = 'Rel'
    Tot = 'Tot'

    @property
    def description(self):
        return self.value


class ADVNumType(Enum):
    Ord = 'Ord'
    Mult = 'Mult'

    @property
    def description(self):
        return self.value


class ADVDegree(Enum):
    Cmp = 'Cmp'
    Pos = 'Pos'
    Sup = 'Sup'

    @property
    def description(self):
        return self.value


class ADVVerbForm(Enum):
    Part = 'Part'

    @property
    def description(self):
        return self.value


class ADVTense(Enum):
    Past = 'Past'
    Pres = 'Pres'

    @property
    def description(self):
        return self.value


class ADVVoice(Enum):
    Act = 'Act'
    Pass = 'Pass'
    Cau = 'Cau'

    @property
    def description(self):
        return self.value


class ADVPolarity(Enum):
    Neg = 'Neg'

    @property
    def description(self):
        return self.value

# Auxiliary verb features


class AUX(Enum):
    Copula = 'Copula'
    Number = 'Number'
    VerbForm = 'VerbForm'
    Mood = 'Mood'
    Tense = 'Tense'
    Voice = 'Voice'
    Polarity = 'Polarity'
    Person = 'Person'
    Polite = 'Polite'

    @property
    def description(self):
        return self.value


class AUXCopula(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class AUXNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value


class AUXVerbForm(Enum):
    Fin = 'Fin'
    Inf = 'Inf'
    Part = 'Part'

    @property
    def description(self):
        return self.value


class AUXMood(Enum):
    Ind = 'Ind'
    Imp = 'Imp'
    Sub = 'Sub'
    Cnd = 'Cnd'

    @property
    def description(self):
        return self.value


class AUXTense(Enum):
    Past = 'Past'
    Pres = 'Pres'

    @property
    def description(self):
        return self.value


class AUXVoice(Enum):
    Act = 'Act'
    Pass = 'Pass'
    Cau = 'Cau'

    @property
    def description(self):
        return self.value


class AUXPolarity(Enum):
    Neg = 'Neg'

    @property
    def description(self):
        return self.value


class AUXPerson(Enum):
    First = '1'
    Second = '2'
    Third = '3'

    @property
    def description(self):
        return self.value


class AUXPolite(Enum):
    Form = 'Form'

    @property
    def description(self):
        return self.value


# Deteminative features

class DET(Enum):
    PronType = 'PronType'
    NumType = 'NumType'
    Reflex = 'Reflex'
    Poss = "Poss"
    Number = "Number"


class DETPronType(Enum):
    Dem = 'Dem'
    Emp = 'Emp'
    Exc = 'Exc'
    Ind = 'Ind'
    Int = 'Int'
    Neg = 'Neg'
    Rel = 'Rel'
    Tot = 'Tot'

    @property
    def description(self):
        return self.value

# Noun features


class NOUN(Enum):
    Number = 'Number'
    Case = 'Case'
    Definite = 'Definite'
    VerbForm = 'VerbForm'
    Tense = 'Tense'
    Voice = 'Voice'
    Polarity = 'Polarity'
    Animacy = 'Animacy'


class NOUNNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value


class NOUNCase(Enum):
    Nom = 'Nom'
    Acc = 'Acc'

    @property
    def description(self):
        return self.value


class NOUNDefinite(Enum):
    Ind = 'Ind'
    Spec = 'Spec'
    Def = 'Def'

    @property
    def description(self):
        return self.value


class NOUNVerbForm(Enum):

    Part = 'Part'
    Inf = 'Inf'
    Vnoun = 'Vnoun'

    @property
    def description(self):
        return self.value


class NOUNTense(Enum):
    Past = 'Past'
    Pres = 'Pres'

    @property
    def description(self):
        return self.value


class NOUNVoice(Enum):
    Act = 'Act'
    Pass = 'Pass'
    Cau = 'Cau'

    @property
    def description(self):
        return self.value


class NOUNPolarity(Enum):
    Neg = 'Neg'

    @property
    def description(self):
        return self.value


class NOUNAnimacy(Enum):
    Hum = 'Hum'
    Nhum = 'Nhum'
    Anim = 'Anim'
    Inan = 'Inan'

    @property
    def description(self):
        return self.value

# Numeral features


class NUM(Enum):
    PronType = 'PronType'
    NumType = 'NumType'
    Number = 'Number'


class NUMPronType(Enum):
    Dem = 'Dem'
    Ind = 'Ind'
    Int = 'Int'
    Rel = 'Rel'

    @property
    def description(self):
        return self.value


class NUMNumType(Enum):
    Card = 'Card'
    Frac = 'Frac'
    Sets = 'Sets'

    @property
    def description(self):
        return self.value


class NUMNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value

# Particle features


class PART(Enum):
    PartType = 'PartType'


class PARTPartType(Enum):
    Verbal = 'Verbal'
    Poss = 'Poss'
    Neg = 'Neg'

    @property
    def description(self):
        return self.value

# Pronoun features


class PRON(Enum):
    PronType = 'PronType'
    Poss = 'Poss'
    Reflex = 'Reflex'
    Number = 'Number'
    Person = 'Person'
    Polite = 'Polite'


class PRONPronType(Enum):
    Dem = 'Dem'
    Emp = 'Emp'
    Exc = 'Exc'
    Ind = 'Ind'
    Int = 'Int'
    Neg = 'Neg'
    Rel = 'Rel'
    Tot = 'Tot'

    @property
    def description(self):
        return self.value


class PRONPoss(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class PRONReflex(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class PRONNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value


class PRONPerson(Enum):
    First = '1'
    Second = '2'
    Third = '3'

    @property
    def description(self):
        return self.value


class PRONPolite(Enum):
    Form = 'Form'

    @property
    def description(self):
        return self.value

# Punctuation features


class PUNCT (Enum):
    PunctSide = 'PunctSide'
    Hyph = 'Hyph'


class PUNCTPunctSide(Enum):
    Ini = 'Ini'
    Fin = 'Fin'

    @property
    def description(self):
        return self.value


class PUNCTHyph(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value

# Verb features


class VERB(Enum):
    Number = 'Number'
    VerbForm = 'VerbForm'
    Mood = 'Mood'
    Tense = 'Tense'
    Voice = 'Voice'
    Person = 'Person'


class VERBNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

    @property
    def description(self):
        return self.value


class VERBVerbForm(Enum):
    Fin = 'Fin'
    Inf = 'Inf'
    Part = 'Part'

    @property
    def description(self):
        return self.value


class VERBMood(Enum):
    Ind = 'Ind'
    Imp = 'Imp'
    Sub = 'Sub'
    Opt = 'Opt'

    @property
    def description(self):
        return self.value


class VERBTense(Enum):
    Past = 'Past'
    Pres = 'Pres'

    @property
    def description(self):
        return self.value


class VERBVoice(Enum):
    Act = 'Act'
    Pass = 'Pass'
    Cau = 'Cau'

    @property
    def description(self):
        return self.value


class VERBPerson(Enum):
    First = '1'
    Second = '2'
    Third = '3'

    @property
    def description(self):
        return self.value


class VERBPolite(Enum):
    Form = 'Form'

    @property
    def description(self):
        return self.value


class X(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value
