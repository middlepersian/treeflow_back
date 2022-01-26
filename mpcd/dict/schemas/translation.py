from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import Translation, Language
from mpcd.dict.schemas import LanguageInput


class TranslationNode(DjangoObjectType):
    class Meta:
        model = Translation
        filter_fields = {'meaning': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class TranslationInput(InputObjectType):
    meaning = String()
    language = LanguageInput()


# Queries

class Query(ObjectType):
    translation = relay.Node.Field(TranslationNode)
    all_translations = DjangoFilterConnectionField(TranslationNode)

# Mutations


class CreateTranslation(relay.ClientIDMutation):
    class Input:
        meaning = String(required=True)
        language = LanguageInput()

    translation = Field(TranslationNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, meaning, id, language):
        # check that Definition  does not exist
        if Translation.objects.filter(id=id).exists():
            return cls(success=False)

        else:
            translation_instance = Translation.objects.create(meaning=meaning)
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language)
                translation_instance.language = language_instance
            translation_instance.save()
            return cls(translation=translation_instance, success=True)


class UpdateTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        meaning = String(required=True)
        language = LanguageInput()

    translation = Field(TranslationNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, meaning, language):
        # check that Definition  does not exist
        if Translation.objects.filter(id=id).exists():
            translation_instance = Translation.objects.get(id=id)
            translation_instance.meaning = meaning
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language)
                translation_instance.language = language_instance
            translation_instance.save()
            return cls(translation=translation_instance, success=True)
        else:
            return cls(success=False)


class DeleteTranslation(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Translation.objects.filter(id=id).exists():
            translation_instance = Translation.objects.get(id=id)
            translation_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutations(ObjectType):
    create_translation = CreateTranslation.Field()
    update_translation = UpdateTranslation.Field()
    delete_translation = DeleteTranslation.Field()
