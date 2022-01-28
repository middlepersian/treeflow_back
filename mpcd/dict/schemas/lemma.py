from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.dict.models import Lemma, Language
from mpcd.dict.schemas import LanguageInput


class LemmaNode(DjangoObjectType):
    class Meta:
        model = Lemma
        filter_fields = {'word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LemmaInput(InputObjectType):
    word = String()
    language = LanguageInput()


# Queries
class Query(ObjectType):
    lemma = relay.Node.Field(LemmaNode)
    all_lemmas = DjangoFilterConnectionField(LemmaNode)

# Mutations


class CreateLemma(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = LanguageInput()

    word = Field(LemmaNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, word, language):
        # check that Definition  does not exist
        if Lemma.objects.filter(word=word).exists():
            return cls(success=False)

        else:
            word_instance = Lemma.objects.create(word=word)
            if Language.objects.filter(identifier=language.identifier).exists():
                language_instance = Language.objects.get(identifier=language.identifier)
                word_instance.language = language_instance
            word_instance.save()
            return cls(word=word_instance, success=True)


class UpdateLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String()
        language = LanguageInput()
    word = Field(LemmaNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, word, id, language, translations):
        # check that Definition  does not exist
        if Lemma.objects.filter(id=id).exists():
            return cls(success=False)

        else:
            word_instance = Lemma.objects.create(word=word)
            if Language.objects.filter(pk=from_global_id(language.id)[1]).exists():
                language_instance = Language.objects.get(pk=from_global_id(language.id)[1])
                word_instance.language = language_instance
            word_instance.save()
            return cls(word=word_instance, success=True)


class DeleteLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Lemma.objects.filter(pk=from_global_id(id)[1]).exists():
            word_instance = Lemma.objects.get(pk=from_global_id(id)[1])
            word_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_lemma = CreateLemma.Field()
    update_lemma = UpdateLemma.Field()
    delete_lemma = DeleteLemma.Field()
