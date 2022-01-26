from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from mpcd.dict.models import LoanWord, Translation, Language
from mpcd.dict.schemas import LanguageInput, TranslationInput


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
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language)
                loanword_instance.language = language_instance
            for translation in translations:
                if Translation.objects.filter(id=translation.id).exists():
                    translation_instance = Translation.objects.get(id=translation.id)
                    loanword_instance.translations.add(translation_instance)
                else:
                    translation_instance = Translation.objects.create(meaning=translation.meaning)
                    if Language.objects.filter(id=translation.language.id).exists():
                        language_instance = Language.objects.get(id=translation.language.id)
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
        if LoanWord.objects.filter(id=id).exists():
            loanword_instance = LoanWord.objects.get(id=id)
            loanword_instance.word = word
            if Language.objects.filter(id=language.id).exists():
                language_instance = Language.objects.get(id=language.id)
                loanword_instance.language = language_instance
            for translation in translations:
                if Translation.objects.filter(id=translation.id).exists():
                    translation_instance = Translation.objects.get(id=translation.id)
                    translation_instance.meaning = translation.meaning
                    if Language.objects.filter(id=translation.language.id).exists():
                        language_instance = Language.objects.get(id=translation.language.id)
                        translation_instance.language = language_instance
                    translation_instance.save()
                    loanword_instance.translations.add(translation_instance)
                else:
                    translation_instance = Translation.objects.create(meaning=translation.meaning)
                    if Language.objects.filter(id=translation.language.id).exists():
                        language_instance = Language.objects.get(id=translation.language.id)
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
        if LoanWord.objects.filter(id=id).exists():
            loanword_instance = LoanWord.objects.get(id=id)
            loanword_instance.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_loanword = CreateLoanWord.Field()
    update_loanword = UpdateLoanWord.Field()
    delete_loanword = DeleteLoanWord.Field()
