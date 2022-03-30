from cgitb import text
from importlib.metadata import requires
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Translation
from mpcd.utils.normalize import to_nfc


class TranslationNode(DjangoObjectType):
    class Meta:
        model = Translation
        filter_fields = {'text': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class TranslationInput(InputObjectType):
    text = String(required=True)
    language = String(required=True)


# Queries

class Query(ObjectType):
    translation = relay.Node.Field(TranslationNode)
    all_translations = DjangoFilterConnectionField(TranslationNode)

    @login_required
    def resolve_all_translations(self, info, **kwargs):
        return gql_optimizer.query(Translation.objects.all(), info)


# Mutations


class CreateTranslation(relay.ClientIDMutation):
    class Input:
        text = String(required=True)
        language = String(required=True)

    translation = Field(TranslationNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, **input):

        # check if translation exists, if not create it
        translation_instance, translation_created = Translation.objects.get_or_create(
            text=to_nfc(input.get('text')), language=to_nfc(input.get('language')))

        return cls(translation=translation_instance, success=True, errors=None)


class UpdateTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        text = String(required=True)
        language = String(required=True)

    translation = Field(TranslationNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, **input):
        # check that translation does exist

        if Translation.objects.filter(pk=from_global_id(id)[1]).exists():
            translation_instance = Translation.objects.get(pk=from_global_id(id)[1])
            # update text
            translation_instance.text = to_nfc(input.get('text'))
            # update language
            translation_instance.lang = to_nfc(input.get('language'))
            # save
            translation_instance.save()
            return cls(translation=translation_instance, success=True)
        else:
            return cls(errors=['Translation ID does not exist'], success=False)


class DeleteTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @login_required

    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Translation.objects.filter(pk=from_global_id(id)[1]).exists():
            translation_instance = Translation.objects.get(pk=from_global_id(id)[1])
            translation_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_translation = CreateTranslation.Field()
    update_translation = UpdateTranslation.Field()
    delete_translation = DeleteTranslation.Field()
