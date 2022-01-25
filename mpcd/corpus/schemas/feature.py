from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Feature


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FeatureNode(DjangoObjectType):
    class Meta:
        model = Feature
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class FeatureInput(InputObjectType):
    identifier = String()


class Query(ObjectType):
    feature = relay.Node.Field(FeatureNode)
    all_feature = DjangoFilterConnectionField(FeatureNode)

# Mutations


class CreateFeature(relay.ClientIDMutation):
    class Input:
        identifier = String()

    feature = Field(FeatureNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if Feature.objects.filter(identifier=identifier).exists():
            return cls(success=False)
        else:
            feature = Feature.objects.create(identifier=identifier)
            return cls(feature=feature, success=True)


class UpdateFeature(relay.ClientIDMutation):
    class Input:
        identifier = String()

    feature = Field(FeatureNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if Feature.objects.filter(identifier=identifier).exists():
            feature = Feature.objects.get(identifier=identifier)
            feature.identifier = identifier
            feature.save()
            return cls(feature=feature, success=True)
        else:
            return cls(success=False)


class DeleteFeature(relay.ClientIDMutation):
    class Input:
        identifier = String()

    feature = Field(FeatureNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if Feature.objects.filter(identifier=identifier).exists():
            feature = Feature.objects.get(identifier=identifier)
            feature.delete()
            return cls(feature=feature, success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_feature = CreateFeature.Field()
    update_feature = UpdateFeature.Field()
    delete_feature = DeleteFeature.Field()
