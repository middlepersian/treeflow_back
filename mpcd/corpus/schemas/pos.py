from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.corpus.models import POS

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class POSNode(DjangoObjectType):
    class Meta:
        model = POS
        filter_fields = {'identifier': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class POSInput(InputObjectType):
    identifier = String()

 # Queries


class Query(ObjectType):
    pos = relay.Node.Field(POSNode)
    all_pos = DjangoFilterConnectionField(POSNode)

# Mutations


class CreatePos(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)

    pos = Field(POSNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):
        # check that pos does not exist
        if POS.objects.filter(identifier=identifier).exists():
            return cls(success=False)

        else:
            pos_instance = POS.objects.create(identifier=identifier)
            pos_instance.save()

            return cls(pos=pos_instance, success=True)

# Update not needed for Pos, there is a closed list available at the model


class DeletePos(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if POS.objects.filter(pk=from_global_id(id)[1]).exists():
            pos_instance = POS.objects.get(pk=from_global_id(id)[1])
            pos_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_pos = CreatePos.Field()
    delete_pos = DeletePos.Field()
