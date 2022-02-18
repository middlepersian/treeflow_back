from distutils import errors
from graphene import relay, InputObjectType, String, Field, ObjectType, List, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from mpcd.dict.models import Dictionary, Lemma, Entry, Translation, Definition, Language, Category, Reference, LoanWord
from mpcd.dict.schemas import DictionaryInput, LemmaInput, LoanWordInput, TranslationInput, DefinitionInput, CategoryInput, ReferenceInput


class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        filter_fields = {'id': ['exact', 'icontains', 'istartswith'],
                         'dict__slug': ['exact', 'icontains', 'istartswith'],
                         'lemma__word': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class EntryInput(InputObjectType):
    dict = DictionaryInput()
    lemma = LemmaInput()
    loanwords = List(LoanWordInput)
    translations = List(TranslationInput)
    definitions = List(DefinitionInput)
    categories = List(CategoryInput)
    references = List(ReferenceInput)
    comment = String()

# Queries


class Query(ObjectType):
    entry = relay.Node.Field(EntryNode)
    all_entries = DjangoFilterConnectionField(EntryNode)

# Mutations


class CreateEntry(relay.ClientIDMutation):
    class Input:
        dict = DictionaryInput()
        lemma = LemmaInput()
        loanwords = List(LoanWordInput)
        translations = List(TranslationInput)
        definitions = List(DefinitionInput)
        categories = List(CategoryInput)
        references = List(ReferenceInput)
        related_entries = List(String)
        comment = String()

    entry = Field(EntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        # check if dict exists
        if Dictionary.objects.filter(slug=input['dict']['slug']).exists():
            dict = Dictionary.objects.get(slug=input['dict']['slug'])
        else:
            return cls(success=False, entry=None, errors=["Dictionary does not exist"])

        # check if lemma exists
        if input.get('lemma', None) is not None:
            if input.get('lemma').get('word', None) is not None:
                lemma_word = input.get('lemma').get('word')
                if input.get('lemma').get('language') is not None:
                    lemma_lang = input.get('lemma', None).get('language')
                    lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)
                    lemma.save()
                    return cls(word=lemma, success=True)
                else:
                    return cls(entry=None, success=False, errors=["No language provided"])
            else:
                return cls(entry=None, success=False, errors=["No word provided"])

        # create entry
        entry = Entry.objects.create(dict=dict, lemma=lemma)

        # check if loanwords exist
        if input.get('loanwords', None) is not None:

            for loanword in input.get('loanwords'):
                if loanword.get('word') is not None:
                    lemma_word = input.get('word')

                if loanword.get('language') is not None:
                    lemma_lang = loanword.get('language')
                    loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                        word=lemma_word, language=lemma_lang)
                    loanword_instance.save()

                if loanword.get('translations', None) is not None:
                    for translation in loanword.get('translations'):
                        # check if translation exists, if not create it
                        translation_instance, translation_created = Translation.objects.get_or_create(
                            text=translation.get('text'), language=translation.get('language'))
                        # add translation
                        loanword_instance.translations.add(translation_instance)
                        loanword_instance.save()

                entry.loanwords.add(loanword_instance)

        # check if translations exist
        if input.get('translations', None) is not None:
            for translation in input.get('translations', None):
                # check if translation exists, if not create it
                translation_instance, translation_created = Translation.objects.get_or_create(
                    text=translation.get('text'), language=translation.get('language'))
                entry.translations.add(translation_instance)

        # check if definitions exist
        if input.get('definitions', None) is not None:
            for definition in input['definitions']:

                if input.get('definition', None) is not None:
                    definition_input = definition.get('definition')

                if definition.get('language', None) is not None:
                    language_input = definition.get('language')
                    definition_instance, definition_created = Definition.objects.get_or_create(
                        definition=definition_input, language=language_input)
                    entry.definitions.add(definition_instance)

                else:
                    return cls(entry=None, success=False, errors=['language for definition is required'])

        if input['categories']:
            for category in input['categories']:
                if Category.objects.filter(category=category['category']).exists():
                    category_obj = Category.objects.get(category=category['category'])
                else:
                    category_obj = Category.objects.create(category=category['category'])
                entry.categories.add(category_obj)
        if input['references']:
            for reference in input['references']:
                if Reference.objects.filter(reference=reference['reference']).exists():
                    reference_obj = Reference.objects.get(reference=reference['reference'])
                else:
                    reference_obj = Reference.objects.create(reference=reference['reference'])
                entry.references.add(reference_obj)

        if input['related_entries']:
            for related_entry in input['related_entries']:
                if Entry.objects.filter(pk=from_global_id(related_entry.id)[1]).exists():
                    related_entry_obj = Entry.objects.get(pk=from_global_id(related_entry.id)[1])
                    entry.related_entries.add(related_entry_obj)

        if input['comment']:
            entry.comment = input['comment']

        entry.save()
        return cls(entry=entry, success=True)


class UpdateEntry(relay.ClientIDMutation):
    class Input:
        id = String()
        dict = DictionaryInput()
        lemma = LemmaInput()
        loanwords = List(LoanWordInput)
        translations = List(TranslationInput)
        definitions = List(DefinitionInput)
        categories = List(CategoryInput)
        references = List(ReferenceInput)
        comment = String()

    entry = Field(EntryNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['id'])[1])

            if input.get('dict', None) is not None:
                if Dictionary.objects.filter(slug=input['dict']['slug']).exists():
                    dict = Dictionary.objects.get(slug=input['dict']['slug'])
                else:
                    return cls(success=False)
                entry.dict = dict

            # update lemma
            if input.get('lemma', None) is not None:
                if input.get('lemma', None).get('word', None) is not None:
                    lemma_word = input.get('lemma', None).get('word')
                    if input.get('language') is not None:
                        lemma_lang = input.get('lemma', None).get('language')
                        lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)
                        lemma.save()
                        entry.lemma = lemma
                        return cls(word=lemma, success=True)
                else:
                    return cls(entry=None, success=False, errors=["No word provided"])

            if input.get('loanwords', None) is not None:
                entry.loanwords.clear()
                for loanword in input.get('loanwords'):
                    if loanword.get('word') is not None:
                        lemma_word = input.get('word')
                    if loanword.get('language') is not None:
                        lemma_lang = loanword.get('language')
                        loanword_instance, loanword_created = LoanWord.objects.get_or_create(
                            word=lemma_word, language=lemma_lang)
                        loanword_instance.save()
                    if loanword.get('translations', None) is not None:
                        for translation in loanword.get('translations'):
                            # check if translation exists, if not create it
                            translation_instance, translation_created = Translation.objects.get_or_create(
                                text=translation.get('text'), language=translation.get('language'))
                            # add translation
                            loanword_instance.translations.add(translation_instance)
                            loanword_instance.save()
                    entry.loanwords.add(loanword_instance)
            if input.get('translations', None) is not None:
                entry.translations.clear()
                for translation in input.get('translations', None):
                    # check if translation exists, if not create it
                    translation_instance, translation_created = Translation.objects.get_or_create(
                        text=translation.get('text'), language=translation.get('language'))
                    entry.translations.add(translation_instance)

            # check if definitions exist
            if input.get('definitions', None) is not None:
                entry.definitions.clear()
                for definition in input['definitions']:

                    if input.get('definition', None) is not None:
                        definition_input = definition.get('definition')

                    if definition.get('language', None) is not None:
                        language_input = definition.get('language')
                        definition_instance, definition_created = Definition.objects.get_or_create(
                            definition=definition_input, language=language_input)
                        entry.definitions.add(definition_instance)

                    else:
                        return cls(entry=None, success=False, errors=['language for definition is required'])

            if input['categories']:
                entry.categories.clear()
                for category in input['categories']:
                    if Category.objects.filter(category=category['category']).exists():
                        category_obj = Category.objects.get(category=category['category'])
                    else:
                        category_obj = Category.objects.create(category=category['category'])
                    entry.categories.add(category_obj)

            if input['references']:
                entry.references.clear()
                for reference in input['references']:
                    if Reference.objects.filter(reference=reference['reference']).exists():
                        reference_obj = Reference.objects.get(reference=reference['reference'])
                    else:
                        reference_obj = Reference.objects.create(reference=reference['reference'])
                    entry.references.add(reference_obj)

            if input['related_entries']:
                entry.related_entries.clear()
                for related_entry in input['related_entries']:
                    if Entry.objects.filter(pk=from_global_id(related_entry.id)[1]).exists():
                        related_entry_obj = Entry.objects.get(pk=from_global_id(related_entry.id)[1])
                        entry.related_entries.add(related_entry_obj)

            if input['comment']:
                entry.comment = input['comment']
            entry.save()
            return cls(entry=entry, success=True)
        else:
            return cls(success=False)


class DeleteEntry(relay.ClientIDMutation):
    class Input:
        id = String()

    success = Boolean()

    @ classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['id'])[1])
            entry.delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(object):
    create_entry = CreateEntry.Field()
    update_entry = UpdateEntry.Field()
    delete_entry = DeleteEntry.Field()
