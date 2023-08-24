import strawberry
import strawberry_django
from strawberry import relay
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from treeflow.corpus import models
from treeflow.corpus.types.pos import POSInput
from treeflow.corpus.enums.pos import UPOSValues
from treeflow.corpus.enums.features import upos_feature_feature_value


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


@strawberry_django.type(models.Feature)
class Feature(relay.Node):
    id: relay.NodeID[str]
    token:  strawberry.LazyType['Token', 'treeflow.corpus.types.token']
    pos : strawberry.LazyType['POS', 'treeflow.corpus.types.pos']
    feature: strawberry.auto
    feature_value: strawberry.auto

@strawberry_django.input(models.Feature)
class FeatureInput:
    token: strawberry.auto
    pos: Optional[POSInput]
    feature: strawberry.auto
    feature_value: strawberry.auto

@strawberry_django.partial(models.Feature)
class FeaturePartial(strawberry_django.NodeInputPartial):
    id: relay.NodeID[str]
    token:  strawberry.auto
    pos: Optional[POSInput]
    feature: strawberry.auto
    feature_value: strawberry.auto
