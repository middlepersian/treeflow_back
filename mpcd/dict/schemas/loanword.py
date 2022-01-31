from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.dict.models import LoanWord, Translation, Language
from mpcd.dict.schemas import LanguageInput, TranslationInput


# TODO check if language IDs inside trnalsation are valid

class LoanWordNode(DjangoObjectType):
    class Meta:
        model = LoanWord
        filter_fields = {'word': ['exact', 'icontains', 'istartswith'],
                         'translations': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LoanWordInput(InputObjectType):
    word = String()
    language = LanguageInput()
    translations = List(TranslationInput)


# Queries
class Query(ObjectType):
    loanword = relay.Node.Field(LoanWordNode)
    all_loanwords = DjangoFilterConnectionField(LoanWordNode)

# Mutations


class CreateLoanWord(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = LanguageInput()
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, word, id, language, translations):
        # check that Definition  does not exist
        if LoanWord.objects.filter(id=id).exists():
            return cls(success=False)

        else:
            loanword_instance = LoanWord.objects.create(word=word)
            if Language.objects.filter(pk=from_global_id(language.id)[1]).exists():
                language_instance = Language.objects.get(pk=from_global_id(language.id)[1])
                loanword_instance.language = language_instance
            for translation in translations:
                if Translation.objects.filter(pk=from_global_id(translation.id)[1]).exists():
                    translation_instance = Translation.objects.get(pk=from_global_id(translation.id)[1])
                    loanword_instance.translations.add(translation_instance)
                else:
                    translation_instance = Translation.objects.create(meaning=translation.meaning)
                    language_instance, language_created = Language.objects.get_or_create(
                        identifier=translation.language.identifier)
                    translation_instance.language = language_instance
                    translation_instance.save()
                    loanword_instance.translations.add(translation_instance)
            loanword_instance.save()
            return cls(loanword=loanword_instance, success=True)


class UpdateLoanWord(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String(required=True)
        language = LanguageInput()
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, word, language, translations):
        # check that Definition  does not exist
        if LoanWord.objects.filter(pk=from_global_id(id)[1]).exists():
            loanword_instance = LoanWord.objects.get(pk=from_global_id(language.id)[1])
            loanword_instance.word = word
            if Language.objects.filter(pk=from_global_id(language.id)[1]).exists():
                language_instance = Language.objects.get(pk=from_global_id(language.id)[1])
                loanword_instance.language = language_instance
            for translation in translations:
                if Translation.objects.filter(pk=from_global_id(language.id)[1]).exists():
                    translation_instance = Translation.objects.get(pk=from_global_id(language.id)[1])
                    translation_instance.meaning = translation.meaning
                    if Language.objects.filter(pk=from_global_id(translation.language.id)[1]).exists():
                        language_instance, language_created = Language.objects.get_or_create(
                            pk=from_global_id(translation.language.id)[1])
                        translation_instance.language = language_instance
                    translation_instance.save()
                    loanword_instance.translations.add(translation_instance)
                else:
                    translation_instance = Translation.objects.create(meaning=translation.meaning)
                    if Language.objects.filter(id=translation.language.id).exists():
                        language_instance, language_created = Language.objects.get_or_create(
                            pk=from_global_id(translation.language.id)[1])
                        translation_instance.language = language_instance
                    translation_instance.save()
                    loanword_instance.translations.add(translation_instance)
            loanword_instance.save()
            return cls(loanword=loanword_instance, success=True)


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
