from graphene import relay, ObjectType, String, Field, ID, Boolean, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import SectionType

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required, superuser_required


class SectionTypeNode(DjangoObjectType):
    class Meta:
        model = SectionType
        filter_fields = {
            'identifier': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class SectionTypeInput(InputObjectType):

    identifier = String()


# Queries

class Query(ObjectType):
    section_type = relay.Node.Field(SectionTypeNode)
    all_section_types = DjangoFilterConnectionField(SectionTypeNode)

    @login_required
    def resolve_all_section_types(self, info, **kwargs):
        return gql_optimizer.query(SectionType.objects.all(), info)


# Mutations

class CreateSectionType(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)

    success = Boolean()
    section_type = Field(SectionTypeNode)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, identifier):
        if SectionType.objects.filter(identifier=identifier).exists():
            return cls(success=False)

        else:
            section_type_instance = SectionType.objects.create(identifier=identifier)
            section_type_instance.save()
            return cls(section_type=section_type_instance, success=True)


class UpdateSectionType(relay.ClientIDMutation):
    class Input:
        identifier = String(required=True)

    success = Boolean()
    section_type = Field(SectionTypeNode)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, id, identifier):
        if SectionType.objects.filter(pk=from_global_id(id[1])).exists():
            section_type_instance = SectionType.objects.get(pk=from_global_id(id[1]))
            section_type_instance.identifier = identifier
            section_type_instance.save()
            return cls(section_type=section_type_instance, success=True)
        else:
            return cls(sucess=False)


class DeleteSectionType(relay.ClientIDMutation):
    class Input:
        id = ID()

    success = Boolean()

    @superuser_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if SectionType.objects.filter(pk=from_global_id(id[1])).exists():
            section_type_instance = SectionType.objects.get(pk=from_global_id(id[1]))
            section_type_instance.delete()
            return cls(success=True)
        else:
            return cls(sucess=False)


class Mutation(ObjectType):
    create_section_type = CreateSectionType.Field()
    delete_section_Type = DeleteSectionType.Field()
    update_section_type = UpdateSectionType.Field()
