from enum import StrEnum

class Deprel(StrEnum):
    ACL = 'acl'
    ACL_CLEFT = 'acl:cleft'
    ACL_RELCL = 'acl:relcl'
    ADVCL = 'advcl'
    ADVCL_CLEFT = 'advcl:cleft'
    ADVMOD = 'advmod'
    ADVMOD_EMPH = 'advmod:emph'
    ADVMOD_LMOD = 'advmod:lmod'
    ADVMOD_TMOD = 'advmod:tmod'
    AMOD = 'amod'
    APPOS = 'appos'
    AUX = 'aux'
    AUX_PASS = 'aux:pass'
    CASE = 'case'
    CC = 'cc'
    CC_NC = 'cc:nc'
    CC_PRECONJ = 'cc:preconj'
    CCOMP = 'ccomp'
    COMPOUND_LVC = 'compound:lvc'
    COMPOUND_REDUP = 'compound:redup'
    COMPOUND_SVC = 'compound:svc'
    CONJ = 'conj'
    COP = 'cop'
    CSUBJ = 'csubj'
    CSUBJ_PASS = 'csubj:pass'
    DEP = 'dep'
    DET = 'det'
    DET_POSS = 'det:poss'
    DISCOURSE = 'discourse'
    DISLOCATED = 'dislocated'
    DISLOCATED_RES = 'dislocated:res'
    DISLOCATED_TOPIC = 'dislocated:topic'
    EXPL = 'expl'
    FIXED = 'fixed'
    FLAT = 'flat'
    GOESWITH = 'goeswith'
    IOBJ = 'iobj'
    MARK = 'mark'
    NMOD = 'nmod'
    NSUBJ = 'nsubj'
    NSUBJ_EMPH = 'nsubj:emph'
    NSUBJ_OUTER = 'nsubj:outer'
    NSUBJ_PASS = 'nsubj:pass'
    NSUBJ_XSUBJ = 'nsubj:xsubj'
    NUMMOD = 'nummod'
    OBJ = 'obj'
    OBJ_EMPH = 'obj:emph'
    OBL = 'obl'
    OBL_AGENT = 'obl:agent'
    OBL_EMPH = 'obl:emph'
    OBL_LMOD = 'obl:lmod'
    OBL_TMOD = 'obl:tmod'
    ORPHAN = 'orphan'
    PARATAXIS = 'parataxis'
    PUNCT = 'punct'
    REPARANDUM = 'reparandum'
    REPARANDUM_RES = 'reparandum:res'
    ROOT = 'root'
    VOCATIVE = 'vocative'
    XCOMP = 'xcomp'
    REF= 'ref'
