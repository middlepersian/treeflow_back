from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Optional

from treeflow.corpus import models

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



@strawberry.type
class UPOSFeatures:
    upos: str
    features: List[str]
    feature_values: List[str]

    @strawberry.field
    def resolve_upos(self, info) -> str:
        return self.upos

    @strawberry.field
    def resolve_features(self, info, feature: Optional[str] = None) -> List[str]:
        feature_names = upos_feature_feature_value.get(self.upos, {})
        if feature:
            feature_values = feature_names.get(feature, [])
            return [feature] if feature_values else []
        return list(feature_names.keys())

    @strawberry.field
    def resolve_feature_values(self, info, upos: str, feature: str) -> List[str]:
        feature_values = upos_feature_feature_value.get(upos, {}).get(feature, ())
        return list(feature_values)


@gql.django.type(models.Feature)
class Feature(relay.Node):

    token_morphological_annotation: relay.Connection[gql.LazyType['Token', 'treeflow.corpus.types.token']]

    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto


@gql.django.input(models.Feature)
class FeatureInput:
    feature: gql.auto
    feature_value: gql.auto

@gql.django.partial(models.Feature)
class FeaturePartial(gql.NodeInputPartial):
    id: relay.GlobalID
    feature: gql.auto
    feature_value: gql.auto