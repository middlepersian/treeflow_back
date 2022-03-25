from cgitb import text
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer

from mpcd.dict.models import Translation


class TranslationNode(DjangoObjectType):
    class Meta:
        model = Translation
        filter_fields = {'text': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class TranslationInput(InputObjectType):
    text = String()
    language = String()


# Queries

class Query(ObjectType):
    translation = relay.Node.Field(TranslationNode)
    all_translations = DjangoFilterConnectionField(TranslationNode)

    def resolve_all_translations(self, info, **kwargs):
        return gql_optimizer.query(Translation.objects.all(), info)


# Mutations


class CreateTranslation(relay.ClientIDMutation):
    class Input:
        text = String(required=True)
        language = ID()

    translation = Field(TranslationNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('text', None) is not None:
            translation_text = input.get('text')
            if input.get('language', None) is not None:
                translation_lang = input.get('language')
                # check if translation exists, if not create it
                translation_instance, translation_created = Translation.objects.get_or_create(
                    text=translation_text, language=translation_lang)
                if not translation_created:
                    return cls(translation=translation_instance, success=False, errors=['Translation already exists'])
                translation_instance.save()
                return cls(translation=translation_instance, success=True, errors=None)
        else:
            return cls(translation=None, errors=['No text provided'], success=False)


class UpdateTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        text = String(required=True)
        language = ID()

    translation = Field(TranslationNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # check that translation does exist
        if input.get('id', None) is not None:
            if Translation.objects.filter(pk=from_global_id(id)[1]).exists():
                translation_instance = Translation.objects.get(pk=from_global_id(id)[1])
                # update text
                if input.get('text', None) is not None:
                    translation_instance.text = input.get('text')
                # update language
                if input.get('language', None) is not None:
                    translation_instance.text = input.get('language')
                translation_instance.save()
                return cls(translation=translation_instance, success=True)
            else:
                return cls(errors=['Translation ID does not exist'], success=False)

        else:
            return cls(success=False, errors=['No ID provided'])


class DeleteTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
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
