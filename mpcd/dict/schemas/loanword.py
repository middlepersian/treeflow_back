from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.dict.models import LoanWord, Translation
from mpcd.dict.schemas import TranslationInput


# TODO check if language IDs inside trnalsation are valid

class LoanWordNode(DjangoObjectType):
    class Meta:
        model = LoanWord
        filter_fields = {'word': ['exact', 'icontains', 'istartswith'],
                         'translations': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LoanWordInput(InputObjectType):
    word = String()
    language = String()
    translations = List(TranslationInput)


# Queries
class Query(ObjectType):
    loanword = relay.Node.Field(LoanWordNode)
    all_loanwords = DjangoFilterConnectionField(LoanWordNode)

# Mutations


class CreateLoanWord(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = String(required=True)
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('word') is not None:
            lemma_word = input.get('word')
        if input.get('language') is not None:
            lemma_lang = input.get('language')
            loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                word=lemma_word, language=lemma_lang)
            # if false, then the object already exists
            if not loanword_created:
                return cls(loanword=None, success=False, errors=['loanword already exists'])
        else:
            return cls(loanword=None, success=False, errors=["No language provided"])

        if input.get('translations', None) is not None:
            for translation_input in input.get('translations'):
                # check if translation exists, if not create it
                translation_instance, translation_created = Translation.objects.get_or_create(
                    text=translation_input.get('text'), language=translation_input.get('language'))
                # add translation to sentence
                loanword_instance.translations.add(translation_instance)
        loanword_instance.save()
        return cls(loanword=loanword_instance, success=True)


class UpdateLoanWord(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String(required=True)
        language = String()
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('id', None) is not None:

            if LoanWord.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                loanword_instance = LoanWord.objects.get(pk=from_global_id(input.get('id'))[1])

                if input.get('word') is not None:
                    lemma_word = input.get('word')
                    loanword_instance.word = lemma_word
                if input.get('language') is not None:
                    lemma_lang = input.get('language')
                    loanword_instance.language = lemma_lang

                if input.get('translations', None) is not None:
                    loanword_instance.translations.clear()
                    for translation_input in input.get('translations'):
                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=translation_input.get('text'), language=translation_input.get('language'))
                        # add translation to sentence
                        loanword_instance.translations.add(translation_instance)
                loanword_instance.save()
                return cls(loanword=loanword_instance, success=True)

        else:
            return cls(loanword=None, success=False, errors=["No id provided"])


class DeleteLoanWord(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        # check that Definition  does not exist
        if LoanWord.objects.filter(pk=from_global_id(id)[1]).exists():
            loanword_instance = LoanWord.objects.get(pk=from_global_id(id)[1])
            loanword_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_loanword = CreateLoanWord.Field()
    update_loanword = UpdateLoanWord.Field()
    delete_loanword = DeleteLoanWord.Field()
