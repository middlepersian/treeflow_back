from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List

from treeflow.corpus.types.feature import Feature, FeatureInput, FeaturePartial,PartOfSpeechFeatures, UPOSFeatures, UPOSList, get_features, upos_feature_feature_value

from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    IsAuthenticated,
)
import strawberry

@gql.type
class Query:
    feature: Optional[Feature] = gql.django.node(directives=[IsAuthenticated()])
    features:  relay.Connection[Feature] = gql.django.connection(directives=[IsAuthenticated()])

    @strawberry.field
    def get_features(self, pos: str) -> PartOfSpeechFeatures:
        feature_values = []
        for feature, values in get_features(pos).items():
            feature_values.append(UPOSFeatures(name=feature, values=values))
            
        return PartOfSpeechFeatures(pos=pos, features=list(get_features(pos).keys()), feature_values=feature_values)
    
    @strawberry.field
    def pos_list(self, info) -> UPOSList:
        pos_list = list(upos_feature_feature_value.keys())
        return UPOSList(pos=pos_list)


@gql.type
class Mutation:
    create_feature: Feature = gql.django.create_mutation(
        FeatureInput, directives=[IsAuthenticated()])
    update_feature: Feature = gql.django.update_mutation(
        FeaturePartial, directives=[IsAuthenticated()])
    delete_feature: Feature = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
