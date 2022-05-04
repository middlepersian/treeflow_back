from app_backend.mpcd.dict.models import loanword
from app_backend.mpcd.dict.schemas.loanword import LoanWordInput
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Lemma, LoanWord, Translation
from mpcd.dict.schemas import LoanWordInput
from mpcd.utils.normalize import to_nfc


class LemmaNode(DjangoObjectType):
    class Meta:
        model = Lemma
        filter_fields = {'word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LemmaInput(InputObjectType):
    word = String(required=True)
    language = String(required=True)
    loanwords = List(LoanWordInput)
    related_lemmas = List(LemmaNode)
    comment = String()


# Queries
class Query(ObjectType):
    lemma = relay.Node.Field(LemmaNode)
    all_lemmas = DjangoFilterConnectionField(LemmaNode)

    @login_required
    def resolve_all_lemmas(self, info, **kwargs):
        return gql_optimizer.query(Lemma.objects.all(), info)

# Mutations


class CreateLemma(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = String(required=True)
        loanwords = List(LoanWordInput)
        related_lemmas = List(LemmaNode)

    word = Field(LemmaNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(
            input.get('word')), language=to_nfc(input.get('language')))

        # loanwords
        if input.get('loanwords', None):
            for loanword in input.get('loanwords'):
                lemma_word = loanword.get('word')
                lemma_lang = loanword.get('language')
                loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                    word=to_nfc(lemma_word), language=to_nfc(lemma_lang))

                if loanword.get('translations', None):
                    # clear up
                    loanword_instance.translations.clear()

                    for translation in loanword.get('translations'):
                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=to_nfc(translation.get('text')), language=translation.get('language'))
                        # add translation
                        loanword_instance.translations.add(translation_instance)
                        loanword_instance.save()

                lemma.loanwords.add(loanword_instance)

        # related_lemmas
        if input.get('related_lemmas', None):
            for related_lemma in input.get('related_lemmas'):
                lemma_rel, lemma_rel_created = Lemma.objects.get_or_create(word=to_nfc(
                    related_lemma.get('word')), language=to_nfc(related_lemma.get('language')))
                lemma.related_lemmas.add(lemma_rel)

        # comment
        if input.get('comment', None):
            lemma.comment = input.get('comment')

        lemma.save()

        return cls(word=lemma, success=True)


class UpdateLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        word = String(required=True)
        language = String(required=True)
        related_lemmas = List(LemmaNode)

    errors = List(String)
    word = Field(LemmaNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if Lemma.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            lemma = Lemma.objects.get(id=from_global_id(input.get('id'))[1])
            lemma.word = to_nfc(input.get('word'))
            lemma.language = to_nfc(input.get('language'))

            # loanwords
            if input.get('loanwords', None):
                # clear up
                lemma.loanwords.clear()
                for loanword in input.get('loanwords'):
                    lemma_word = loanword.get('word')
                    lemma_lang = loanword.get('language')
                    loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                        word=to_nfc(lemma_word), language=to_nfc(lemma_lang))

                    if loanword.get('translations', None):
                        # clear up
                        loanword_instance.translations.clear()

                        for translation in loanword.get('translations'):
                            # check if translation exists, if not create it
                            translation_instance, translation_created = Translation.objects.get_or_create(
                                text=to_nfc(translation.get('text')), language=translation.get('language'))
                            # add translation
                            loanword_instance.translations.add(translation_instance)
                            loanword_instance.save()

                    lemma.loanwords.add(loanword_instance)

            # related_lemmas
            if input.get('related_lemmas', None):
                # clear up
                lemma.related_lemmas.clear()
                for related_lemma in input.get('related_lemmas'):
                    lemma_rel, lemma_rel_created = Lemma.objects.get_or_create(word=to_nfc(
                        related_lemma.get('word')), language=to_nfc(related_lemma.get('language')))
                    lemma.related_lemmas.add(lemma_rel)

            # comment
            if input.get('comment', None):
                lemma.comment = input.get('comment')

            lemma.save()

            return cls(word=lemma, success=True)
        else:
            return cls(token=None, success=False, errors=["Lemma ID does not exists"])


class DeleteLemma(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    @login_required
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
