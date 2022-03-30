from graphene import relay, InputObjectType, String, Field, ObjectType, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Reference


class ReferenceNode(DjangoObjectType):
    class Meta:
        model = Reference
        filter_fields = {'reference': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class ReferenceInput(InputObjectType):
    reference = String()
    url = String()


# Queries
class Query(ObjectType):
    reference = relay.Node.Field(ReferenceNode)
    all_references = DjangoFilterConnectionField(ReferenceNode)

    @login_required
    def resolve_all_references(self, info, **kwargs):
        return gql_optimizer.query(Reference.objects.all(), info)

# Mutations


class CreateReference(relay.ClientIDMutation):
    class Input:
        reference = ReferenceInput()
        url = String()

    reference = Field(ReferenceNode)
    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, reference, id, url):
        # check that Reference  does not exist
        if Reference.objects.filter(pk=from_global_id(id)[1]).exists():
            return cls(success=False)

        else:
            reference_instance = Reference.objects.create(reference=reference)
            reference_instance.url = url
            reference_instance.save()
            return cls(reference=reference_instance, success=True)


class UpdateReference(relay.ClientIDMutation):
    class Input:
        reference = ReferenceInput()
        url = String()

    reference = Field(ReferenceNode)
    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, reference, id, url):
        # check that Reference  does not exist
        if Reference.objects.filter(pk=from_global_id(id)[1]).exists():
            reference_instance = Reference.objects.get(pk=from_global_id(id)[1])
            reference_instance.reference = reference
            reference_instance.url = url
            reference_instance.save()
            return cls(reference=reference_instance, success=True)

        else:
            return cls(success=False)


class DeleteReference(relay.ClientIDMutation):
    class Input:
        reference = ReferenceInput()

    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, reference, id):
        # check that Reference  does not exist
        if Reference.objects.filter(pk=from_global_id(id)[1]).exists():
            reference_instance = Reference.objects.get(pk=from_global_id(id)[1])
            reference_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_reference = CreateReference.Field()
    update_reference = UpdateReference.Field()
    delete_reference = DeleteReference.Field()
