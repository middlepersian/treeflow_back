from graphene import relay, InputObjectType, String, Field, ObjectType, List, ID, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import LoanWord, Translation
from mpcd.dict.schemas import TranslationInput
from mpcd.utils.normalize import to_nfc


# TODO check if language IDs inside trnalsation are valid

class LoanWordNode(DjangoObjectType):
    class Meta:
        model = LoanWord
        filter_fields = {'word': ['exact', 'icontains', 'istartswith'],
                         'translations': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LoanWordInput(InputObjectType):
    word = String(required=True)
    language = String(required=True)
    translations = List(TranslationInput)


# Queries
class Query(ObjectType):
    loanword = relay.Node.Field(LoanWordNode)
    all_loanwords = DjangoFilterConnectionField(LoanWordNode)

    @login_required
    def resolve_all_loanwords(self, info, **kwargs):
        return gql_optimizer.query(LoanWord.objects.all(), info)

# Mutations


class CreateLoanWord(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = String(required=True)
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        loanword_instance, loanword_created = LoanWord.objects.get_or_create(
            word=to_nfc(input.get('word')), language=to_nfc(input.get('language')))

        if input.get('translations', None) is not None:
            for translation_input in input.get('translations'):
                # check if translation exists, if not create it
                translation_instance, translation_created = Translation.objects.get_or_create(
                    text=to_nfc(input.get('text')), language=to_nfc(input.get('language')))
                # add translation to sentence
                loanword_instance.translations.add(translation_instance)
        loanword_instance.save()
        return cls(loanword=loanword_instance, success=True)


class UpdateLoanWord(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String(required=True)
        language = String(required=True)
        translations = List(TranslationInput)

    loanword = Field(LoanWordNode)
    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('id', None) is not None:

            if LoanWord.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
                loanword_instance = LoanWord.objects.get(pk=from_global_id(input.get('id'))[1])
                loanword_instance.word = to_nfc(input.get('word'))
                loanword_instance.language = to_nfc(input.get('language'))

                if input.get('translations', None) is not None:
                    loanword_instance.translations.clear()
                    for translation_input in input.get('translations'):
                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=to_nfc(input.get('text')), language=to_nfc(input.get('language')))
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

    @login_required
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
