from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional

from treeflow.corpus.types.feature import Feature, FeatureInput, FeaturePartial, UPOSFeatures, upos_feature_feature_value

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
    def upos_features(self, info, upos: str, feature: Optional[str] = None) -> UPOSFeatures:
        feature_names = upos_feature_feature_value.get(upos, {})
        features = list(feature_names.keys())
        if feature is not None:
            feature_values = [', '.join(feature_names.get(feature, []))]
        else:
            feature_values = [', '.join(feature_names.get(feat, [])) for feat in features]
        return UPOSFeatures(upos=upos, features=features, feature_values=feature_values)





@gql.type
class Mutation:
    create_feature: Feature = gql.django.create_mutation(
        FeatureInput, directives=[IsAuthenticated()])
    update_feature: Feature = gql.django.update_mutation(
        FeaturePartial, directives=[IsAuthenticated()])
    delete_feature: Feature = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
