from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer

from mpcd.dict.models import Lemma


class LemmaNode(DjangoObjectType):
    class Meta:
        model = Lemma
        filter_fields = {'word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LemmaInput(InputObjectType):
    word = String()
    language = String()


# Queries
class Query(ObjectType):
    lemma = relay.Node.Field(LemmaNode)
    all_lemmas = DjangoFilterConnectionField(LemmaNode)
    def resolve_all_lemmas(self, info, **kwargs):
        return gql_optimizer.query(Lemma.objects.all(), info)    

# Mutations


class CreateLemma(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = String()

    word = Field(LemmaNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if input.get('word') is not None:
            lemma_word = input.get('word')
            if input.get('language') is not None:
                lemma_lang = input.get('language')
                lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)
                if lemma_created:
                    lemma.save()
                    return cls(word=lemma, success=True)
                else:
                    return cls(word=None, success=False, errors=['Lemma already exists'])
            else:
                return cls(token=None, success=False, errors=["No language provided"])
        else:
            return cls(token=None, success=False, errors=["No word provided"])


class UpdateLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String()
        language = String()

    errors = List(String)
    word = Field(LemmaNode)
    success = Boolean()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('id') is not None:
            lemma = Lemma.objects.get(id=from_global_id(input.get('id'))[1])
            if input.get('word') is not None:
                lemma_word = input.get('word')
                lemma.word = lemma_word
            if input.get('language') is not None:
                lemma_lang = input.get('language')
                lemma.language = lemma_lang
            lemma.save()
            return cls(word=lemma, success=True)
        else:
            return cls(token=None, success=False, errors=["No id provided"])


class DeleteLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @ classmethod
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
