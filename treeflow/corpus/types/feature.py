from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from treeflow.corpus import models
from treeflow.corpus.types.pos import POSInput

import strawberry


upos_feature_feature_value = {
    'ADV': {
        'Deixis': ('Prox', 'Remt')
    },
    'DET': {
        'Definite': ('Ind', 'Spec'),
        'PronType': ('Dem', 'Ind', 'Tot', 'Int'),
        'Deixis': ('Prox', 'Remt')
    },
    'PUNCT': {
        'PunctType': ('Semi', 'Dash', 'Excl', 'Quot'),
        'PunctSide': ('Ini', 'Fin')
    },
    'SCONJ': {
        'PronType': ('Rel',)
    },
    'NUM': {
        'NumType': ('Card', 'Fract', 'Sets')
    },
    'PART': {
        'PartType': ('Mod', 'Neg', 'Emp', 'Vbp')
    },
    'PRON': {
        'PronType': ('Prs', 'Dem', 'Int', 'Rel', 'Tot', 'Ing', 'Neg', 'Exc'),
        'Person': ('1', '2', '3'),
        'Number': ('Sing', 'Plur'),
        'Case': ('Nom', 'Acc'),
        'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
        'Deixis': ('Prox', 'Remt')
    },
    'NOUN': {
        'Number': ('Sing', 'Plur'),
        'Polite': ('Inform', 'Form', 'Elev', 'Humb'),
        'Animacy': ('Hum', 'Nhum', 'Inan'),
        'Gender': ('Fem', 'Masc'),
        'Case': ('Nom', 'Acc'),
        'Subcat': ('Tran',),
        'VerbForm': ('Inf', 'Part', 'Vnoun')
    },
    'PROPN': {
        'NameType': ('Giv', 'Pat', 'Geo', 'Oth'),
        'Transc': ('Yes',)
    },
    'SYM': {
        'Text': ()
    },
    'AUX': {
        'VerbType': ('Cop', 'Quasi', 'Light', 'Mod'),
        'Subcat': ('Tran', 'Intr'),
        'Tense': ('Pres', 'Past'),
        'Mood': ('Ind', 'Sub', 'Opt', 'Imp', 'Nec'),
        'Person': ('1', '2', '3'),
        'Number': ('Sing', 'Plur'),
        'VerbForm': ('Fin', 'Inf', 'Conv'),
        'Polarity': ('Neg',)
    }
}

def get_features(pos: str ) -> Dict[str, Tuple[str]]:
    pos_features = upos_feature_feature_value
    return pos_features.get(pos, {})

@strawberry.type
class UPOSList:
    pos: List[str]
    
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
    feature: gql.auto
    feature_value: gql.auto