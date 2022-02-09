from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import FeatureValue


# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class FeatureValueNode(DjangoObjectType):
    class Meta:
        model = FeatureValue
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class FeatureValueInput(InputObjectType):
    identifier = String()


class Query(ObjectType):
    featurevalue = relay.Node.Field(FeatureValueNode)
    all_featurevalue = DjangoFilterConnectionField(FeatureValueNode)

# Mutations
class CreateFeatureValue(relay.ClientIDMutation):
    class Input:
        identifier = String()

    featurevalue = Field(FeatureValueNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if FeatureValue.objects.filter(identifier=identifier).exists():
            return cls(success=False)
        else:
            featurevalue = FeatureValue.objects.create(identifier=identifier)
            featurevalue.save()
            return cls(featurevalue=featurevalue, success=True)


class UpdateFeatureValue(relay.ClientIDMutation):
    class Input:
        identifier = String()

    featurevalue = Field(FeatureValueNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if FeatureValue.objects.filter(identifier=identifier).exists():
            featurevalue = FeatureValue.objects.get(identifier=identifier)
            featurevalue.identifier = identifier
            featurevalue.save()
            return cls(featurevalue=featurevalue, success=True)
        else:
            return cls(success=False)


class DeleteFeatureValue(relay.ClientIDMutation):
    class Input:
        identifier = String()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):

        if FeatureValue.objects.filter(identifier=identifier).exists():
            featurevalue = FeatureValue.objects.get(identifier=identifier)
            featurevalue.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_featurevalue = CreateFeatureValue.Field()
    update_featurevalue = UpdateFeatureValue.Field()
    delete_featurevalue = DeleteFeatureValue.Field()
