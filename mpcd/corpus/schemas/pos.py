from graphene import relay, ObjectType, String, Field, ID, Boolean, List, Int, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.corpus.models import Pos

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class PosNode(DjangoObjectType):
    class Meta:
        model = Pos
        filter_fields = {'pos': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)

    interfaces = (relay.Node,)


class PosInput(InputObjectType):
    pos = String()

 # Queries


class Query(ObjectType):
    pos = relay.Node.Field(PosNode)
    all_pos = DjangoFilterConnectionField(PosNode)

# Mutations


class CreatePos(relay.ClientIDMutation):
    class Input:
        pos = String(required=True)

    pos = Field(PosNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, pos):
        # check that pos does not exist
        if Pos.objects.filter(pos=pos).exists():
            return cls(success=False)

        else:
            pos_instance = Pos.objects.create(pos=pos)

            return cls(pos=pos_instance, success=True)


class UpdatePos(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        pos = String()

    pos = Field(PosNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, pos):
        # check that pos does not exist
        if Pos.objects.filter(pos=pos).exists():
            return cls(success=False)

        else:
            pos_instance = Pos.objects.get(id=id)
            pos_instance.pos = pos
            pos_instance.save()

            return cls(pos=pos_instance, success=True)


class DeletePos(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Pos.objects.filter(id=id).exists():
            pos_instance = Pos.objects.get(id=id)
            pos_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutations(ObjectType):
    create_pos = CreatePos.Field()
    update_pos = UpdatePos.Field()
    delete_pos = DeletePos.Field()
