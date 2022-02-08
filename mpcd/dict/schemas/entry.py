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

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            return cls(success=False)
        else:
            # check if dict exists
            if Dictionary.objects.filter(slug=input['dict']['slug']).exists():
                dict = Dictionary.objects.get(slug=input['dict']['slug'])
            else:
                return cls(success=False)
            # check if word exists
            if Lemma.objects.filter(word=input['lemma']['word']).exists():
                lemma = Lemma.objects.get(word=input['lemma']['word'])
            else:
                lemma = Lemma.objects.create(word=input['lemma']['word'])

            # create entry
            entry = Entry.objects.create(dict=dict, lemma=lemma)

            # check if loanwords exist
            if input['loanwords']:
                for loanword in input['loanwords']:
                    if LoanWord.objects.filter(word=loanword['word']).exists():
                        loanword_obj = LoanWord.objects.get(word=loanword['word'])
                    else:
                        loanword_obj = LoanWord.objects.create(word=loanword['word'])
                        if loanword['language']:
                            if Language.objects.filter(language=loanword['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=loanword['language']['identifier'])
                                loanword_obj.language = language_obj
                             # check if there are translations for the loanword
                            if loanword['translations']:
                                for translation in loanword['translations']:
                                    if Translation.objects.filter(translation=translation['translation']).exists():
                                        translation_obj = Translation.objects.get(
                                            translation=translation['translation'])
                                    else:
                                        translation_obj = Translation.objects.create(
                                            translation=translation['translation'])
                                        if translation['language']:
                                            if Language.objects.filter(language=translation['language']['identifier']).exists():
                                                language_obj = Language.objects.get(
                                                    language=translation['language']['identifier'])
                                                translation_obj.language = language_obj
                                            else:
                                                return cls(success=False)
                                    loanword_obj.translations.add(translation_obj)

                            loanword_obj.save()

                    entry.loanwords.add(loanword_obj)

            # check if translations exist
            if input['translations']:
                for translation in input['translations']:
                    if Translation.objects.filter(word=translation['word']).exists():
                        translation_obj = Translation.objects.get(word=translation['word'])
                    else:
                        translation_obj = Translation.objects.create(word=translation['word'])
                        if translation['language']:
                            if Language.objects.filter(language=translation['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=translation['language']['identifier'])
                                translation_obj.language = language_obj
                            translation_obj.save()
                    entry.translations.add(translation_obj)

            # check if definitions exist
            if input['definitions']:
                for definition in input['definitions']:
                    if Definition.objects.filter(definition=definition['definition']).exists():
                        definition_obj = Definition.objects.get(definition=definition['definition'])
                    else:
                        definition_obj = Definition.objects.create(definition=definition['definition'])
                        # check if there is a language assocaited with the definition
                        if definition['language']:
                            if Language.objects.filter(language=definition['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=definition['language']['identifier'])
                                definition_obj.language = language_obj
                            definition_obj.save()
                    entry.definitions.add(definition_obj)

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

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if Entry.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            entry = Entry.objects.get(pk=from_global_id(input['id'])[1])
            if input['dict']:
                if Dictionary.objects.filter(slug=input['dict']['slug']).exists():
                    dict = Dictionary.objects.get(slug=input['dict']['slug'])
                else:
                    return cls(success=False)
                entry.dict = dict

            if input['lemma']:
                if Lemma.objects.filter(word=input['lemma']['word']).exists():
                    lemma = Lemma.objects.get(word=input['lemma']['word'])
                else:
                    lemma = Lemma.objects.create(word=input['lemma']['word'])
                entry.lemma = lemma

            if input['loanwords']:
                entry.loanwords.clear()
                for loanword in input['loanwords']:
                    if LoanWord.objects.filter(word=loanword['word']).exists():
                        loanword_obj = LoanWord.objects.get(word=loanword['word'])
                    else:
                        loanword_obj = LoanWord.objects.create(word=loanword['word'])
                        if loanword['language']:
                            if Language.objects.filter(language=loanword['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=loanword[' language']['identifier'])
                                loanword_obj.language = language_obj
                    entry.loanwords.add(loanword_obj)

            if input['translations']:
                entry.translations.clear()
                for translation in input['translations']:
                    if Translation.objects.filter(word=translation['word']).exists():
                        translation_obj = Translation.objects.get(word=translation['word'])
                    else:
                        translation_obj = Translation.objects.create(word=translation['word'])
                        if translation['language']:
                            if Language.objects.filter(language=translation['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=translation['language']['identifier'])
                                translation_obj.language = language_obj
                            translation_obj.save()
                    entry.translations.add(translation_obj)

            if input['definitions']:
                entry.definitions.clear()
                for definition in input['definitions']:
                    if Definition.objects.filter(definition=definition['definition']).exists():
                        definition_obj = Definition.objects.get(definition=definition['definition'])
                    else:
                        definition_obj = Definition.objects.create(definition=definition['definition'])
                        if definition['language']:
                            if Language.objects.filter(language=definition['language']['identifier']).exists():
                                language_obj = Language.objects.get(language=definition['language']['identifier'])
                                definition_obj.language = language_obj
                            definition_obj.save()
                    entry.definitions.add(definition_obj)

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
