from graphene import Enum, ObjectType, Field


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
    Mult = 'Mult'

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


class ADVPronType(Enum):

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

    @property
    def description(self):
        return self.value


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


class DETNumType(Enum):
    Ord = 'Ord'
    Mult = 'Mult'

    @property
    def description(self):
        return self.value


class DETReflex(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class DETPoss(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class DETNumber(Enum):
    Sing = 'Sing'
    Plur = 'Plur'

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

    @property
    def description(self):
        return self.value


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

    @property
    def description(self):
        return self.value


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

    @property
    def description(self):
        return self.value


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

    @property
    def description(self):
        return self.value


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
    Foreign = 'Foreign'

    @property
    def description(self):
        return self.value


class XForeign(Enum):
    Yes = 'Yes'

    @property
    def description(self):
        return self.value


class Query(ObjectType):

    # Adjective features
    adj = Field(ADJ, description='Adjective features')
    adj_numtype = Field(ADJNumType, description='Adjective numeral type')
    adj_poss = Field(ADJPoss, description='Adjective possessive')
    adj_number = Field(ADJNumber, description='Adjective number')
    adj_case = Field(ADJCase, description='Adjective case')
    adj_degree = Field(ADJDegree, description='Adjective degree')
    adj_verbform = Field(ADJVerbForm, description='Adjective verb form')
    adj_tense = Field(ADJTense, description='Adjective tense')
    adj_voice = Field(ADJVoice, description='Adjective voice')
    adj_polarity = Field(ADJPolarity, description='Adjective polarity')

    def resolve_adj(root, info, adj):
        return adj

    def resolve_adj_numtype(root, info, adj_numtype):
        return adj_numtype

    def resolve_adj_poss(root, info, adj_poss):
        return adj_poss

    def resolve_adj_number(root, info, adj_number):
        return adj_number

    def resolve_adj_case(root, info, adj_case):
        return adj_case

    def resolve_adj_degree(root, info, adj_degree):
        return adj_degree

    def resolve_adj_verbform(root, info, adj_verbform):
        return adj_verbform

    def resolve_adj_tense(root, info, adj_tense):
        return adj_tense

    def resolve_adj_voice(root, info, adj_voice):
        return adj_voice

    def resolve_adj_polarity(root, info, adj_polarity):
        return adj_polarity

    # Adposition features
    adp = Field(ADP, description='Adposition features')
    adp_poss = Field(ADPPos, description='Adposition position')

    def resolve_adp(root, info, adp):
        return adp

    def resolve_adp_poss(root, info, adp_poss):
        return adp_poss

    # Adverb features
    adv = Field(ADV, description='Adverb features')
    adv_prontype = Field(ADVPronType, description='Adverb pronoun type')
    adv_numtype = Field(ADVNumType, description='Adverb numeral type')
    adv_degree = Field(ADVDegree, description='Adverb degree')
    adv_verbform = Field(ADVVerbForm, description='Adverb verb form')
    adv_tense = Field(ADVTense, description='Adverb tense')
    adv_voice = Field(ADVVoice, description='Adverb voice')
    adv_polarity = Field(ADVPolarity, description='Adverb polarity')

    def resolve_adv(root, info, adv):
        return adv

    def resolve_adv_prontype(root, info, adv_prontype):
        return adv_prontype

    def resolve_adv_numtype(root, info, adv_numtype):
        return adv_numtype

    def resolve_adv_degree(root, info, adv_degree):
        return adv_degree

    def resolve_adv_verbform(root, info, adv_verbform):
        return adv_verbform

    def resolve_adv_tense(root, info, adv_tense):
        return adv_tense

    def resolve_adv_voice(root, info, adv_voice):
        return adv_voice

    def resolve_adv_polarity(root, info, adv_polarity):
        return adv_polarity

    # Auxiliary verb features
    aux = Field(AUX, description='Auxiliary verb features')
    aux_copula = Field(AUXCopula, description='Auxiliary copula')
    aux_number = Field(AUXNumber, description='Auxiliary number')
    aux_verbform = Field(AUXVerbForm, description='Auxiliary verb form')
    aux_voice = Field(AUXVoice, description='Auxiliary voice')
    aux_polarity = Field(AUXPolarity, description='Auxiliary polarity')
    aux_person = Field(AUXPerson, description='Auxiliary person')
    aux_polite = Field(AUXPolite, description='Auxiliary polite')

    def resolve_aux(root, info, aux):
        return aux

    def resolve_aux_copula(root, info, aux_copula):
        return aux_copula

    def resolve_aux_number(root, info, aux_number):
        return aux_number

    def resolve_aux_verbform(root, info, aux_verbform):
        return aux_verbform

    def resolve_aux_voice(root, info, aux_voice):
        return aux_voice

    def resolve_aux_polarity(root, info, aux_polarity):
        return aux_polarity

    def resolve_aux_person(root, info, aux_person):
        return aux_person

    def resolve_aux_polite(root, info, aux_polite):
        return aux_polite

    # Determiner features

    det = Field(DET, description='Determiner features')
    det_prontype = Field(DETPronType, description='Determiner pronoun type')
    det_numtype = Field(DETNumType, description='Determiner numeral type')
    det_reflex = Field(DETReflex, description='Determiner reflexive')
    det_poss = Field(DETPoss, description='Determiner possessive')
    det_number = Field(DETNumber, description='Determiner number')

    def resolve_det(root, info, det):
        return det

    def resolve_det_prontype(root, info, det_prontype):
        return det_prontype

    def resolve_det_numtype(root, info, det_numtype):
        return det_numtype

    def resolve_det_reflex(root, info, det_reflex):
        return det_reflex

    def resolve_det_poss(root, info, det_poss):
        return det_poss

    def resolve_det_number(root, info, det_number):
        return det_number

     # Noun features
    noun = Field(NOUN, description='Noun features')
    noun_number = Field(NOUNNumber, description='Noun number')
    noun_case = Field(NOUNCase, description='Noun case')
    noun_definite = Field(NOUNDefinite, description='Noun definite')
    noun_verbform = Field(NOUNVerbForm, description='Noun verb form')
    noun_tense = Field(NOUNTense, description='Noun tense')
    noun_voice = Field(NOUNVoice, description='Noun voice')
    noun_polarity = Field(NOUNPolarity, description='Noun polarity')
    noun_animacy = Field(NOUNAnimacy, description='Noun animacy')

    def resolve_noun(root, info, noun):
        return noun

    def resolve_noun_number(root, info, noun_number):
        return noun_number

    def resolve_noun_case(root, info, noun_case):
        return noun_case

    def resolve_noun_definite(root, info, noun_definite):
        return noun_definite

    def resolve_noun_verbform(root, info, noun_verbform):
        return noun_verbform

    def resolve_noun_tense(root, info, noun_tense):
        return noun_tense

    def resolve_noun_voice(root, info, noun_voice):
        return noun_voice

    def resolve_noun_polarity(root, info, noun_polarity):
        return noun_polarity

    def resolve_noun_animacy(root, info, noun_animacy):
        return noun_animacy

    # Numeral features
    num = Field(NUM, description='Numeral features')
    num_prontype = Field(NUMPronType, description='Numeral pronoun type')
    num_numtype = Field(NUMNumType, description='Numeral numeral type')
    num_number = Field(NUMNumber, description='Numeral number')

    def resolve_num(root, info, num):
        return num

    def resolve_num_prontype(root, info, num_prontype):
        return num_prontype

    def resolve_num_numtype(root, info, num_numtype):
        return num_numtype

    def resolve_num_number(root, info, num_number):
        return num_number

    # Particle features
    part = Field(PART, description='Particle features')
    part_parttype = Field(PARTPartType, description='Particle particle type')

    def resolve_part(root, info, part):
        return part

    def resolve_part_parttype(root, info, part_parttype):
        return part_parttype

    # Pronoun features
    pron = Field(PRON, description='Pronoun features')
    pron_prontype = Field(PRONPronType, description='Pronoun pronoun type')
    pron_poss = Field(PRONPoss, description='Pronoun possessive')
    pron_reflex = Field(PRONReflex, description='Pronoun reflexive')
    pron_number = Field(PRONNumber, description='Pronoun number')
    pron_person = Field(PRONPerson, description='Pronoun person')
    pron_polite = Field(PRONPolite, description='Pronoun polite')

    def resolve_pron(root, info, pron):
        return pron

    def resolve_pron_prontype(root, info, pron_prontype):
        return pron_prontype

    def resolve_pron_poss(root, info, pron_poss):
        return pron_poss

    def resolve_pron_reflex(root, info, pron_reflex):
        return pron_reflex

    def resolve_pron_number(root, info, pron_number):
        return pron_number

    def resolve_pron_person(root, info, pron_person):
        return pron_person

    def resolve_pron_polite(root, info, pron_polite):
        return pron_polite

    # Punctuation features
    punct = Field(PUNCT, description='Punctuation features')
    punct_punctside = Field(PUNCTPunctSide, description='Punctuation punctuation side')
    punct_hyph = Field(PUNCTHyph, description='Punctuation hyphen')

    def resolve_punct(root, info, punct):
        return punct

    def resolve_punct_punctside(root, info, punct_punctside):
        return punct_punctside

    def resolve_punct_hyph(root, info, punct_hyph):
        return punct_hyph

    # Verb features
    verb = Field(VERB, description='Verb features')
    verb_number = Field(VERBNumber, description='Verb number')
    verb_mood = Field(VERBMood, description='Verb mood')
    verb_tense = Field(VERBTense, description='Verb tense')
    verb_voice = Field(VERBVoice, description='Verb voice')
    verb_person = Field(VERBPerson, description='Verb person')
    verb_polite = Field(VERBPolite, description='Verb polite')

    def resolve_verb(root, info, verb):
        return verb

    def resolve_verb_number(root, info, verb_number):
        return verb_number

    def resolve_verb_mood(root, info, verb_mood):
        return verb_mood

    def resolve_verb_tense(root, info, verb_tense):
        return verb_tense

    def resolve_verb_voice(root, info, verb_voice):
        return verb_voice

    def resolve_verb_person(root, info, verb_person):
        return verb_person

    def resolve_verb_polite(root, info, verb_polite):
        return verb_polite

# X features

    x = Field(X, description='X features')
    x_foreign = Field(XForeign, description='X foreign')

    def resolve_x(root, info, x):
        return x

    def resolve_x_foreign(root, info, x_foreign):
        return x_foreign
