from distutils import errors
from graphene import relay, InputObjectType, String, Field, ObjectType, List, Boolean, ID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Dictionary, Lemma, Entry, Translation, Definition, Category, Reference, LoanWord
from mpcd.dict.schemas import LemmaInput, LoanWordInput, TranslationInput, DefinitionInput, CategoryInput, ReferenceInput

from mpcd.utils.normalize import to_nfc


class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        filter_fields = {'id': ['exact', 'icontains', 'istartswith'],
                         'dict__slug': ['exact', 'icontains', 'istartswith'],
                         'lemma__word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class EntryInput(InputObjectType):
    dict = ID(required=True)
    lemma = LemmaInput(required=True)
    loanwords = List(LoanWordInput)
    translations = List(TranslationInput)
    definitions = List(DefinitionInput)
    categories = List(CategoryInput)
    references = List(ReferenceInput)
    related_entries = List(ID)
    comment = String()

# Queries


class Query(ObjectType):
    entry = relay.Node.Field(EntryNode)
    all_entries = DjangoFilterConnectionField(EntryNode)

    @login_required
    def resolve_all_entries(self, info, **kwargs):
        return gql_optimizer.query(Entry.objects.all(), info)


# Mutations

class CreateEntry(relay.ClientIDMutation):
    class Input:
        dict = ID()
        lemma = LemmaInput(required=True)
        loanwords = List(LoanWordInput)
        translations = List(TranslationInput)
        definitions = List(DefinitionInput)
        categories = List(CategoryInput)
        references = List(ReferenceInput)
        related_entries = List(ID)
        comment = String()

    entry = Field(EntryNode)
    success = Boolean()
    errors = List(String)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # check if dict exists
        if Dictionary.objects.filter(pk=from_global_id(input['dict'])[1]).exists():
            dict = Dictionary.objects.get(pk=from_global_id(input['dict'])[1])
        else:
            return cls(success=False, entry=None, errors=["Dictionary does not exist"])

        # get or create Lemma
        lemma_word = input.get('lemma', None).get('word', None)
        lemma_lang = input.get('lemma', None).get('language', None)
        lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(lemma_word), language=lemma_lang)

        # create entry
        entry, entry_created = Entry.objects.get_or_create(dict=dict, lemma=lemma)

        # check if loanwords exist
        if input.get('loanwords', None) is not None:

            for loanword in input.get('loanwords'):
                lemma_word = input.get('word')
                lemma_lang = loanword.get('language')
                loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                    word=to_nfc(lemma_word), language=lemma_lang)

                if loanword.get('translations', None) is not None:
                    for translation in loanword.get('translations'):
                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=to_nfc(translation.get('text')), language=translation.get('language'))
                        # add translation
                        loanword_instance.translations.add(translation_instance)
                        loanword_instance.save()

                entry.loanwords.add(loanword_instance)
            entry.save()

        # check if translations exist
        if input.get('translations', None) is not None:
            for translation in input.get('translations', None):
                # check if translation exists, if not create it
                translation_instance, translation_created = Translation.objects.get_or_create(
                    text=to_nfc(translation.get('text')), language=translation.get('language'))
                entry.translations.add(translation_instance)
            entry.save()

        # check if definitions exist
        if input.get('definitions', None) is not None:
            for definition in input['definitions']:
                definition_instance, definition_created = Definition.objects.get_or_create(
                    definition=to_nfc(definition.get('definition')), language=translation.get('language'))
                entry.definitions.add(definition_instance)
            entry.save()

        if input.get('categories', None) is not None:
            for category in input['categories']:
                category_obj, category_created = Category.objects.get_or_create(category=category['category'])
                if category_obj:
                    entry.categories.add(category_obj)
            entry.save()

        if input.get('references', None) is not None:
            for reference in input['references']:
                reference_obj = Reference.objects.get_or_create(reference=reference['reference'])
                if reference_obj:
                    entry.references.add(reference_obj)
            entry.save()

        '''
        if input.get('related_entries', None) is not None:
            for related_entry in input['related_entries']:
                if Entry.objects.filter(pk=from_global_id(related_entry.id)[1]).exists():
                    related_entry_obj = Entry.objects.get(pk=from_global_id(related_entry.id)[1])
                    entry.related_entries.add(related_entry_obj)

        '''
        if input.get('comment', None) is not None:
            entry.comment = to_nfc(input.get('comment'))
            entry.comment = input['comment']
            entry.save()

        return cls(entry=entry, success=True)


class UpdateEntry(relay.ClientIDMutation):
    class Input:
        id = ID()
        dict = ID()
        lemma = LemmaInput(required=True)
        loanwords = List(LoanWordInput)
        translations = List(TranslationInput)
        definitions = List(DefinitionInput)
        categories = List(CategoryInput)
        references = List(ReferenceInput)
        comment = String()

    entry = Field(EntryNode)
    success = Boolean()
    errors = List(String)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['id'])[1])

            # update dict
            if input.get('dict', None) is not None:
                if Dictionary.objects.filter(pk=from_global_id(input['id'])[1]).exists():
                    dict = Dictionary.objects.get(pk=from_global_id(input['id'])[1])
                else:
                    return cls(success=False)
                entry.dict = dict

            # update lemma
            lemma_word = input.get('lemma', None).get('word', None)
            lemma_lang = input.get('lemma', None).get('language', None)
            lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(lemma_word), language=lemma_lang)
            entry.lemma = lemma

            # check if loanwords exist
            if input.get('loanwords', None) is not None:

                for loanword in input.get('loanwords'):
                    lemma_word = input.get('word')
                    lemma_lang = loanword.get('language')
                    loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                        word=to_nfc(lemma_word), language=to_nfc(lemma_lang))

                    if loanword.get('translations', None) is not None:
                        for translation in loanword.get('translations'):
                            # check if translation exists, if not create it
                            translation_instance, translation_created = Translation.objects.get_or_create(
                                text=to_nfc(translation.get('text')), language=translation.get('language'))
                            # add translation
                            loanword_instance.translations.add(translation_instance)
                            loanword_instance.save()

                    entry.loanwords.add(loanword_instance)

            # check if translations exist
            if input.get('translations', None) is not None:
                for translation in input.get('translations', None):
                    # check if translation exists, if not create it
                    translation_instance, translation_created = Translation.objects.get_or_create(
                        text=to_nfc(translation.get('text')), language=translation.get('language'))
                    entry.translations.add(translation_instance)

            # check if definitions exist
            if input.get('definitions', None) is not None:
                for definition in input['definitions']:
                    definition_instance, definition_created = Definition.objects.get_or_create(
                        definition=to_nfc(definition.get('definition')), language=translation.get('language'))
                    entry.definitions.add(definition_instance)

            if input.get('categories', None) is not None:
                for category in input['categories']:
                    category_obj, category_created = Category.objects.get_or_create(category=category['category'])
                    if category_obj:
                        entry.categories.add(category_obj)
            if input.get('references', None) is not None:
                for reference in input['references']:
                    reference_obj = Reference.objects.get_or_create(reference=reference['reference'])
                    if reference_obj:
                        entry.references.add(reference_obj)

            if input.get('related_entries', None) is not None:
                for related_entry in input['related_entries']:
                    if Entry.objects.filter(pk=from_global_id(related_entry.id)[1]).exists():
                        related_entry_obj = Entry.objects.get(pk=from_global_id(related_entry.id)[1])
                        entry.related_entries.add(related_entry_obj)

            if input.get('comment', None) is not None:
                entry.comment = input['comment']

            entry.save()
            return cls(entry=entry, success=True)

        else:
            return cls(success=False)


class DeleteEntry(relay.ClientIDMutation):
    class Input:
        id = String()

    success = Boolean()

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['id'])[1])
            entry.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class AddRelatedEntry(relay.ClientIDMutation):

    class Input:
        entry_id = ID(required=True)
        related_entry_id = ID(required=True)

    success = Boolean()
    errors = List(String)
    entry = Field(EntryNode)

    @login_required
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Entry.objects.filter(pk=from_global_id(input['entry_id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['entry_id'])[1])
            if Entry.objects.filter(pk=from_global_id(input['related_entry_id'])[1]).exists():
                related_entry = Entry.objects.get(pk=from_global_id(input['related_entry_id'])[1])
                entry.related_entries.add(related_entry)
                entry.save()
                return cls(entry=entry, success=True, errors=None)
            else:
                return cls(entry=None, success=False, errors=['related entry does not exist'])
        else:
            return cls(entry=None, success=False, errors=['entry does not exist'])


class Mutation(object):
    create_entry = CreateEntry.Field()
    update_entry = UpdateEntry.Field()
    delete_entry = DeleteEntry.Field()
    add_related_entry = AddRelatedEntry.Field()
