from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from treeflow.corpus import models
from treeflow.corpus.types.pos import POSInput
from treeflow.corpus.enums.pos import UPOSValues
from treeflow.corpus.enums.features import upos_feature_feature_value

import strawberry



def get_features(pos: str ) -> Dict[str, Tuple[str]]:
    return upos_feature_feature_value.get(pos, {})

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
