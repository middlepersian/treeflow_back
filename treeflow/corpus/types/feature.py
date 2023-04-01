from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from treeflow.corpus import models
from treeflow.corpus.types.pos import POSInput
from treeflow.corpus.enums.pos import UPOSValues

import strawberry


upos_feature_feature_value = {
 'ADJ': {
  'Number': ('Plur',),
  'Degree': ('Cmp', 'Sup'),
  'NumType': ('Ord', 'Mult'),
  'Subcat': ('Tran', 'Intr'),
  'Tense': ('Pres', 'Past'),
  'VerbForm': ('Part',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'ADP': {'AdpType': ('Prep', 'Post', 'Circ'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'ADV': {
  'AdvType': ('Man', 'Loc', 'Tim', 'Deg'),
  'NumType': ('Card', 'Mult', 'Ord'),
  'Deixis': ('Prox', 'Remt'),
  'Degree': ('Cmp', 'Sup'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),},
 'DET': {
  'Definite': ('Ind', 'Spec'),
  'PronType': ('Dem', 'Ind', 'Tot', 'Int', 'Prs', 'Emp'),
  'Deixis': ('Prox', 'Remt'),
  'Person': ('1', '2', '3'),
  'Number': ('Sing', 'Plur'),
  'Poss': ('Yes',),
  'Refl': ('Yes',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'PUNCT': {
  'PunctType': ('Semi', 'Dash', 'Excl', 'Quot'),
  'PunctSide': ('Ini', 'Fin'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'SCONJ': {
  'PronType': ('Rel',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'NUM': {
  'NumType': ('Card', 'Fract', 'Sets'),
  'Number': ('Plur',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'PART': {
  'PartType': ('Mod', 'Neg', 'Emp', 'Vbp'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'PRON': {'PronType': ('Prs', 'Dem', 'Emp', 'Int', 'Rel', 'Tot', 'Ind', 'Rcp', 'Neg', 'Exc'),
  'Person': ('1', '2', '3'),
  'Number': ('Sing', 'Plur'),
  'Case': ('Nom', 'Acc'),
  'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
  'Deixis': ('Prox', 'Remt'),
  'Poss': ('Yes',), 
  'Refl': ('Yes',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'NOUN': {
  'Number': ('Sing', 'Plur'),
  'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
  'Animacy': ('Hum', 'Nhum', 'Anim', 'Inan'),
  'Gender': ('Fem', 'Masc'),
  'Case': ('Nom', 'Acc'),
  'Subcat': ('Tran', 'Intr'),
  'VerbForm': ('Inf', 'Part', 'Vnoun'),
  'Tense': ('Pres', 'Past'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'PROPN': {'NameType': ('Giv', 'Pat', 'Geo', 'Oth'),
  'Animacy': ('Hum', 'Nhum', 'Anim', 'Inan'),
  'Gender': ('Fem', 'Masc'),
  'Transc': ('Yes',),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',)},
 'SYM': {
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'AUX': {'VerbType': ('Cop', 'Quasi', 'Light', 'Mod'),
  'Subcat': ('Tran', 'Intr'),
  'Tense': ('Pres', 'Past'),
  'Mood': ('Ind', 'Sub', 'Opt', 'Imp', 'Nec'),
  'Person': ('1', '2', '3'),
  'Number': ('Sing', 'Plur'),
  'VerbForm': ('Fin', 'Inf', 'Part', 'Conv', 'Vnoun'),
  'Polarity': ('Neg',),
  'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)},
 'VERB': {'VerbType': ('Cop', 'Quasi', 'Light', 'Mod'),
  'Subcat': ('Tran', 'Intr'),
  'Tense': ('Pres', 'Past'),
  'Mood': ('Ind', 'Sub', 'Opt', 'Imp', 'Nec'),
  'Person': ('1', '2', '3'),
  'Number': ('Sing', 'Plur'),
  'VerbForm': ('Fin', 'Inf', 'Part', 'Conv', 'Vnoun'),
  'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
  'Foreign': ('Yes',),
  'Hyph': ('Yes',),
  'Typo': ('Yes',),
  'Transc': ('Yes',)}
}

def get_features(pos: str ) -> Dict[str, Tuple[str]]:
    pos_features = upos_feature_feature_value
    return pos_features.get(pos, {})

@strawberry.type
class UPOSList:
    pos: List[UPOSValues]
    
@strawberry.type
class UPOSFeatures:
    name: str
    values: Tuple[str]

@strawberry.type
class PartOfSpeechFeatures:
    pos: str
    features: List[str]
    feature_values: List[UPOSFeatures]


@gql.django.type(models.Feature)
class Feature(relay.Node):
    id: relay.GlobalID
    token:  gql.LazyType['Token', 'treeflow.corpus.types.token']
    pos : gql.LazyType['POS', 'treeflow.corpus.types.pos']
    feature: gql.auto
    feature_value: gql.auto

@gql.django.input(models.Feature)
class FeatureInput:
    token: relay.GlobalID
    pos: Optional[POSInput]
    feature: gql.auto
    feature_value: gql.auto

@gql.django.partial(models.Feature)
class FeaturePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    token: relay.GlobalID
    pos: Optional[POSInput]
    feature: gql.auto
    feature_value: gql.auto
