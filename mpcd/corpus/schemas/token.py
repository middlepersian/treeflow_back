from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType, Int, Float
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import F
from graphql_relay import from_global_id
from mpcd.dict.models import Entry, Lemma, Translation, Dictionary
from mpcd.corpus.models import Token, MorphologicalAnnotation, Dependency, Text, Line
from mpcd.corpus.schemas import MorphologicalAnnotationInput
from mpcd.corpus.schemas import DependencyInput
from mpcd.dict.schemas import EntryInput
import graphene_django_optimizer as gql_optimizer

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class TokenNode(DjangoObjectType):
    class Meta:
        model = Token
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith'],
                         'line': ['exact'],
                         }
        interfaces = (relay.Node,)


class TokenInput(InputObjectType):
    text = ID()
    transcription = String()
    transliteration = String()
    language = String()
    lemma = EntryInput()
    pos = String()
    morphological_annotation = List(MorphologicalAnnotationInput)
    syntactic_annotation = List(DependencyInput)
    comment = String()
    avestan = String()
    previous = TokenNode()
    line = ID()
    position_in_line = Int()

# Queries


class Query(ObjectType):
    token = relay.Node.Field(TokenNode)
    all_tokens = DjangoFilterConnectionField(TokenNode)
    #all_tokens = List(TokenNode)

    def resolve_all_tokens(self, info, **kwargs):
        qs = Token.objects.all()
        return gql_optimizer.query(qs, info)

# Mutations


class CreateToken(relay.ClientIDMutation):
    class Input:
        transcription = String(required=True)
        transliteration = String(required=True)
        language = String()
        text = ID(required=True)
        number = Float()
        lemma = EntryInput()
        pos = String()
        morphological_annotation = List(MorphologicalAnnotationInput)
        syntactic_annotation = List(DependencyInput)
        comment = String()
        avestan = String()
        previous = ID()
        line = ID()
        position_in_line = Int()

    token = Field(TokenNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("INPUT: {}".format(input))

        if input.get('transcription', None) is None and input.get('transliteration', None) is None:
            return cls(token=None, success=False, errors=["No transcription or transliteration provided"])
        else:
            token = Token.objects.create(
                transcription=input['transcription'], transliteration=input['transliteration'])

        # check if text available
        if input.get('text', None) is not None:
            if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
                text = Text.objects.get(pk=from_global_id(input['text'])[1])
                token.text = text
            else:
                return cls(token=None, success=False, errors=["Text with ID {} not found".format(input['text'])])

        # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

        # check if lemma available
        if input.get('lemma', None) is not None:

            # get lemmas word
            if input.get('lemma').get('lemma').get('word', None) is not None:
                lemma_word = input.get('lemma').get('lemma').get('word')
                if input.get('lemma').get('lemma').get('language', None) is not None:
                    lemma_lang = input.get('lemma').get('lemma').get('language')

                    lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)
                    lemma.save()

                else:
                    return cls(token=None, success=False, errors=["No language provided for lemma"])

            else:
                return cls(token=None, success=False, errors=["No lemma word provided"])

          # check dict
            if input.get('lemma').get('dict', None) is not None:
                dict = Dictionary.objects.get(pk=from_global_id(input['lemma']['dict'])[1])
                entry, entry_created = Entry.objects.get_or_create(lemma=lemma, dict=dict)
            else:
                return cls(token=None, success=False, errors=["No dictionary provided for lemma"])

            # check if translations available
            if input.get('lemma').get('translations') is not None:
                for translation in input['lemma']['translations']:
                    # check if language in mutation input is available
                    translation_obj, translation_obj_created = Translation.objects.get_or_create(
                        text=translation['text'], language=translation['language'])
                    entry.translations.add(translation_obj)

            entry.save()

            # add the entry to the token
            token.lemma = entry

        # check if number available
        if input.get('number', None) is not None:
            token.number = input['number']
        else:
            return cls(token=None, success=False, errors=["No number provided"])

        # check if pos available
        if input.get('pos', None) is not None:
            token.pos = input.get('pos')

       # check if morphological annotation available
        if input.get('morphological_annotation', None) is not None:
            for annotation in input['morphological_annotation']:
                annotation_obj, annotation_obj_created = MorphologicalAnnotation.objects.get_or_create(
                    feature=annotation['feature'], feature_value=annotation['feature_value'])
                token.morphological_annotation.add(annotation_obj)
        # check if syntactic annotation available
        if input.get('syntactic_annotation') is not None:
            for annotation in input['syntactic_annotation']:
                dep_obj, dep_created = Dependency.objects.get_or_create(head=annotation['head'], rel=annotation['rel'])
                token.syntactic_annotation.add(dep_obj)
        # check if comment available
        if input.get('comment', None) is not None:
            token.comment = input['comment']
        # check if avestan available
        if input.get('avestan', None) is not None:
            token.avestan = input['avestan']
        # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                token.previous = Token.objects.filter(pk=from_global_id(input['previous'])[1]).first()
            else:
                return cls(token=None, success=False, errors=["Previous token with ID {} not found".format(input['previous'])])

        # check if line available
        if input.get('line', None) is not None:
            # check if line with assigned id already exists
            if Line.objects.filter(pk=from_global_id(input['line'])[1]).exists():
                line = Line.objects.filter(pk=from_global_id(input['line'])[1]).first()
                token.line = line
            else:
                return cls(token=None, success=False, errors=["Line with ID {} not found".format(input['line'])])
        # check if position_in_line available
        if input.get('position_in_line', None) is not None:
            position_in_line = input['position_in_line']
            token.position_in_line = position_in_line

        token.save()

        return cls(token=token, success=True)


class UpdateToken(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        transcription = String(required=True)
        transliteration = String(required=True)
        language = String()
        text = ID(required=True)
        number = Float()
        lemma = EntryInput()
        pos = String()
        morphological_annotation = List(MorphologicalAnnotationInput)
        syntactic_annotation = List(DependencyInput)
        comment = String()
        avestan = String()
        previous = ID()
        line = ID()
        position_in_line = Int()

    token = Field(TokenNode)
    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        if input.get('id', None) is not None:
            # check if token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['id'])[1]).exists():
                # get the token
                token = Token.objects.get(pk=from_global_id(input['id'])[1])
            else:
                return cls(token=None, success=False, errors=["Token with ID {} not found".format(input['id'])])

            # check if transcription available
            if input.get('transcription', None) is not None:
                token.transcription = input['transcription']
            # check if transliteration available
            if input.get('transliteration', None) is not None:
                token.transliteration = input['transliteration']
            # check if lemma available
             # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

        # check if lemma available
        if input.get('lemma', None) is not None:

            # get lemmas word
            if input.get('lemma').get('lemma').get('word', None) is not None:
                lemma_word = input.get('lemma').get('lemma').get('word')
                if input.get('lemma').get('lemma').get('language', None) is not None:
                    lemma_lang = input.get('lemma').get('lemma').get('language')

                    lemma, lemma_created = Lemma.objects.get_or_create(word=lemma_word, language=lemma_lang)
                    lemma.save()

                else:
                    return cls(token=None, success=False, errors=["No language provided for lemma"])

            else:
                return cls(token=None, success=False, errors=["No lemma word provided"])

          # check dict
            if input.get('lemma').get('dict', None) is not None:
                dict = Dictionary.objects.get(pk=from_global_id(input['lemma']['dict'])[1])
                entry, entry_created = Entry.objects.get_or_create(lemma=lemma, dict=dict)
            else:
                return cls(token=None, success=False, errors=["No dictionary provided for lemma"])

            # check if translations available
            if input.get('lemma').get('translations') is not None:
                entry.translations.clear()
                for translation in input['lemma']['translations']:
                    # check if language in mutation input is available
                    translation_obj, translation_obj_created = Translation.objects.get_or_create(
                        word=translation['text'], language=translation['language'])
                    entry.translations.add(translation_obj)

            entry.save()

            # add the entry to the token
            token.lemma = entry

        # check if number available
        if input.get('number', None) is not None:
            token.number = input['number']
        else:
            return cls(token=None, success=False, errors=["No number provided"])

        # check if language available
        if input.get('language', None) is not None:
            token.language = input.get('language', None)

        # check if pos available
        if input.get('pos', None) is not None:
            token.pos = input.get('pos')

        # check if morphological annotation available
        if input.get('morphological_annotation', None) is not None:
            token.morphological_annotation.clear()
            for annotation in input['morphological_annotation']:
                annotation_obj, annotation_obj_created = MorphologicalAnnotation.objects.get_or_create(
                    feature=annotation['feature'], feature_value=annotation['feature_value'])
                token.morphological_annotation.add(annotation_obj)
        # check if syntactic annotation available
        if input.get('syntactic_annotation') is not None:
            token.syntactic_annotation.clear()
            for annotation in input['syntactic_annotation']:
                dep_obj, dep_created = Dependency.objects.get_or_create(head=annotation['head'], rel=annotation['rel'])
                token.syntactic_annotation.add(dep_obj)
        # check if comment available
        if input.get('comment', None) is not None:
            token.comment = input['comment']
        # check if avestan available
        if input.get('avestan', None) is not None:
            token.avestan = input['avestan']
        # check if previous token available
        if input.get('previous', None) is not None:
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                token.previous = Token.objects.filter(pk=from_global_id(input['previous'])[1]).first()

           # check if line available
        if input.get('line', None) is not None:
            # check if line with assigned id already exists
            if Line.objects.filter(pk=from_global_id(input['line'])[1]).exists():
                line = Line.objects.get(pk=from_global_id(input['line'])[1])
                token.line = line
            else:
                return cls(token=None, success=False, errors=["Line with ID {} not found".format(input['line'])])

        # check if position_in_line available
        if input.get('position_in_line', None) is not None:
            position_in_line = input['position_in_line']
            token.position_in_line = position_in_line

        # save token
        token.save()
        return cls(token=token, success=True)


class DeleteToken(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        if Token.objects.filter(pk=from_global_id(id)[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(id)[1])
            token_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class JoinTokens(relay.ClientIDMutation):
    class Input():
        current = ID()
        previous = ID()

    success = Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # get token
        if input.get('current', None) is not None:
            if Token.objects.filter(pk=from_global_id(input['current'])[1]).exists():
                current_token = Token.objects.get(pk=from_global_id(input['current'])[1])
            else:
                return cls(success=False, errors=["Token with ID {} not found".format(input['current'])])
            logger.error("TOKEN_ID: {}".format(current_token.id))
        if input.get('previous', None) is not None:
            # get previous token
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                previous_token = Token.objects.get(pk=from_global_id(input['previous'])[1])
                current_token.previous = previous_token
                previous_token.save()
            else:
                return cls(success=False, errors=["Token with ID {} not found".format(input['previous'])])

        return cls(success=True)


class Mutation(ObjectType):
    create_token = CreateToken.Field()
    delete_token = DeleteToken.Field()
    update_token = UpdateToken.Field()
    join_tokens = JoinTokens.Field()
