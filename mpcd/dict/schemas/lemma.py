from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Lemma, Meaning
from mpcd.dict.schemas.language_enum import Language
from mpcd.utils.normalize import to_nfc
from .meaning import MeaningNode


class LemmaNode(DjangoObjectType):
    class Meta:
        model = Lemma
        filter_fields = {'word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class LemmaInput(InputObjectType):
    word = String(required=True)
    language = Language(required=True)
    related_lemmas = List(ID, required=True)
    related_meanings = List(ID, required=True)


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
        language = Language(required=True)
        related_lemmas = List(ID, required=True)
        related_meanings = List(ID, required=True)

    lemma = Field(LemmaNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(
            input.get('word')), language=to_nfc(input.get('language')))

        # related_lemmas

        for related_lemma in input.get('related_lemmas'):
            lemma_rel = Lemma.objects.get(id=from_global_id(related_lemma)[1])
            lemma.related_lemmas.add(lemma_rel)

        # related_meanings

        for related_meaning in input.get('related_meanings'):
            meaning_rel = Meaning.objects.get(id=from_global_id(related_meaning)[1])
            lemma.related_meanings.add(meaning_rel)

        lemma.save()

        return cls(lemma=lemma, success=True)


class UpdateLemma(relay.ClientIDMutation):
    class Input:
        word = String(required=True)
        language = Language(required=True)
        related_lemmas = List(ID, required=True)
        related_meanings = List(ID, required=True)
        comments = List(ID, required=True)

    errors = List(String)
    lemma = Field(LemmaNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        if Lemma.objects.filter(pk=from_global_id(input.get('id'))[1]).exists():
            lemma = Lemma.objects.get(id=from_global_id(input.get('id'))[1])
            lemma.word = to_nfc(input.get('word'))
            lemma.language = to_nfc(input.get('language'))

            # related_lemmas
            # clear up
            lemma.related_lemmas.clear()
            for related_lemma in input.get('related_lemmas'):
                lemma_rel = Lemma.objects.get(id=from_global_id(related_lemma)[1])
                lemma.related_lemmas.add(lemma_rel)

            # related_meanings
            # clear up
            lemma.related_lemmas.clear()
            for related_meaning in input.get('related_meanings'):
                meaning_rel = Meaning.objects.get(
                    id=from_global_id(related_meaning)[1])
                lemma.related_meanings.add(meaning_rel)

            # comments
            # clear up
            lemma.comments.clear()
            for comment in input.get('comments'):
                comment_rel = Comment.objects.get(id=from_global_id(comment)[1])
                lemma.comments.add(comment_rel)

            lemma.save()

            return cls(lemma=lemma, success=True)
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


class AddRelatedLemmaToLemma (relay.ClientIDMutation):
    class Input:
        source_id = ID(required=True)
        related_id = ID(required=True)

    success = Boolean()
    errors = List(String)

    source = Field(LemmaNode)
    related = Field(LemmaNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, source_id, related_id):

        if Lemma.objects.filter(pk=from_global_id(source_id)[1]).exists():
            source_lemma_instance = Lemma.objects.get(pk=from_global_id(source_id)[1])

        else:
            return cls(success=False, errors=["Source Lemma ID does not exists"], source=None, related=None)

        if Lemma.objects.filter(pk=from_global_id(related_id)[1]).exists():
            related_lemma_instance = Lemma.objects.get(pk=from_global_id(related_id)[1])

            source_lemma_instance.related_lemmas.add(related_lemma_instance)
            source_lemma_instance.save()

            return cls(success=True, errors=None, source=source_lemma_instance, related=related_lemma_instance)

        else:
            return cls(success=False, errors=["Related Lemma ID does not exists"], source=None, related=None)


class RemoveRelatedLemmaFromLemma(relay.ClientIDMutation):
    class Input:
        source_id = ID(required=True)
        related_id = ID(required=True)

    success = Boolean()
    errors = List(String)

    source = Field(LemmaNode)
    related = Field(LemmaNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, source_id, related_id):

        if Lemma.objects.filter(pk=from_global_id(source_id)[1]).exists():
            source_lemma_instance = Lemma.objects.get(pk=from_global_id(source_id)[1])

        else:
            return cls(success=False, errors=["Source Lemma ID does not exists"], source=None, related=None)

        if Lemma.objects.filter(pk=from_global_id(related_id)[1]).exists():
            related_lemma_instance = Lemma.objects.get(pk=from_global_id(related_id)[1])

            source_lemma_instance.related_lemmas.remove(related_lemma_instance)
            source_lemma_instance.save()

            return cls(success=True, errors=None, source=source_lemma_instance, related=related_lemma_instance)

        else:
            return cls(success=False, errors=["Related Lemma ID does not exists"], source=None, related=None)


class AddRelatedMeaningToLemma(relay.ClientIDMutation):
    class Input:
        lemma_id = ID(required=True)
        meaning_id = ID(required=True)

    success = Boolean()
    errors = List(String)

    lemma = Field(LemmaNode)
    meaning = Field(MeaningNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, lemma_id, meaning_id):
        if Lemma.objects.filter(pk=from_global_id(lemma_id)[1]).exists():
            lemma_instance = Lemma.objects.get(pk=from_global_id(lemma_id)[1])

        else:
            return cls(success=False, errors=["Lemma ID does not exists"], lemma=None, meaning=None)

        if Meaning.objects.filter(pk=from_global_id(meaning_id)[1]).exists():
            meaning_instance = Meaning.objects.get(pk=from_global_id(meaning_id)[1])
        else:
            return cls(success=False, errors=["Meaning ID does not exists"], lemma=None, meaning=None)

        # add meaning to lemma
        lemma_instance.related_meanings.add(meaning_instance)
        lemma_instance.save()
        return cls(lemma=lemma_instance, meaning=meaning_instance, success=True, errors=None)


class RemoveRelatedMeaningFromLemma(relay.ClientIDMutation):
    class Input:
        lemma_id = ID(required=True)
        meaning_id = ID(required=True)

    success = Boolean()
    errors = List(String)

    lemma = Field(LemmaNode)
    meaning = Field(MeaningNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, lemma_id, meaning_id):
        if Lemma.objects.filter(pk=from_global_id(lemma_id)[1]).exists():
            lemma_instance = Lemma.objects.get(pk=from_global_id(lemma_id)[1])

        else:
            return cls(success=False, errors=["Lemma ID does not exists"], lemma=None, meaning=None)

        if Meaning.objects.filter(pk=from_global_id(lemma_id)[1]).exists():
            meaning_instance = Meaning.objects.get(pk=from_global_id(meaning_id)[1])
        else:
            return cls(success=False, errors=["Meaning ID does not exists"], lemma=None, meaning=None)

        # add meaning to lemma
        lemma_instance.related_meanings.remove(meaning_instance)
        lemma_instance.save()
        return cls(lemma=lemma_instance, meaning=meaning_instance, success=True, errors=None)


class Mutation(ObjectType):
    # TODO add_related_lemma_to_lemma
    add_related_lemma_to_lemma = AddRelatedLemmaToLemma.Field()
    remove_related_lemma_from_lemma = RemoveRelatedLemmaFromLemma.Field()
    add_related_meaning_to_lemma = AddRelatedMeaningToLemma.Field()
    remove_related_meaning_from = RemoveRelatedMeaningFromLemma.Field()
    create_lemma = CreateLemma.Field()
    update_lemma = UpdateLemma.Field()
    delete_lemma = DeleteLemma.Field()
