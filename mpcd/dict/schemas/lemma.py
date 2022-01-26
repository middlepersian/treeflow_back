from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
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
    word = relay.Node.Field(LemmaNode)
    all_words = DjangoFilterConnectionField(LemmaNode)

# Mutations

class CreateWord(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
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
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language)
                word_instance.language = language_instance
            word_instance.save()
            return cls(word=word_instance, success=True)                

class UpdateWord(relay.ClientIDMutation):
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
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language)
                word_instance.language = language_instance
            word_instance.save()
            return cls(word=word_instance, success=True)

class DeleteWord(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
    
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if Lemma.objects.filter(id=id).exists():
            word_instance = Lemma.objects.get(id=id)
            word_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)           

class Mutations(ObjectType):
    create_word = CreateWord.Field()
    update_word = UpdateWord.Field()
    delete_word = DeleteWord.Field()            