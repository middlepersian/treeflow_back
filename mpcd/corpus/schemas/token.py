from graphene import relay, ObjectType, String, Field, ID, Boolean, List, InputObjectType, Int, Float, UUID
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
from mpcd.corpus.models import Token, MorphologicalAnnotation, Dependency, Text, Line, CommentCategory
from mpcd.dict.models import Lemma, Meaning
from mpcd.corpus.schemas import MorphologicalAnnotationInput
from mpcd.corpus.schemas import DependencyInput
from mpcd.corpus.schemas.pos_enum import POS
from mpcd.dict.schemas.language_enum import Language
from mpcd.dict.schemas.lemma import LemmaNode
from mpcd.corpus.schemas.comment_category_enum import CommentCategories

import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from mpcd.utils.normalize import to_nfc

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

# TODO update schemas and normalize


class TokenNode(DjangoObjectType):
    class Meta:
        model = Token
        filter_fields = {'transcription': ['exact', 'icontains', 'istartswith'],
                         'transliteration': ['exact', 'icontains', 'istartswith'],
                         'line': ['exact'],
                         'text__id': ['exact']
                         }
        interfaces = (relay.Node,)


class TokenInput(InputObjectType):
    text = ID(required=True)
    transcription = String(required=True)
    transliteration = String(required=True)
    number = Float(required=True)
    language = Language(required=True)
    lemmas = List(ID, required=True)
    meanings = List(ID, required=True)
    pos = POS(required=False)
    morphological_annotation = List(MorphologicalAnnotationInput, required=True)
    syntactic_annotation = List(DependencyInput, required=True)
    comment = String(required=False)
    uncertain = List(CommentCategories, required=True)
    to_discuss = List(CommentCategories, required=True)
    new_suggestion = List(CommentCategories, required=True)
    avestan = String(required=False)
    previous = ID(required=False)
    line = ID(required=False)
    position_in_line = Int(required=False)

# Queries


class Query(ObjectType):
    token = relay.Node.Field(TokenNode)
    all_tokens = DjangoFilterConnectionField(TokenNode)

    @login_required
    def resolve_all_tokens(self, info, **kwargs):
        qs = Token.objects.all()
        return gql_optimizer.query(qs, info)

# Mutations


class CreateToken(relay.ClientIDMutation):
    class Input:
        text = ID(required=True)
        transcription = String(required=True)
        transliteration = String(required=True)
        number = Float(required=True)
        language = Language(required=True)
        lemmas = List(ID, required=True)
        meanings = List(ID, required=True)
        pos = POS(required=False)
        morphological_annotation = List(MorphologicalAnnotationInput, required=True)
        syntactic_annotation = List(DependencyInput, required=True)
        comment = String(required=False)
        uncertain = List(CommentCategories, required=True)
        to_discuss = List(CommentCategories, required=True)
        new_suggestion = List(CommentCategories, required=True)
        avestan = String(required=False)
        previous = ID(required=False)
        line = ID(required=False)
        position_in_line = Int(required=False)

    token = Field(TokenNode)
    errors = List(String)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("INPUT: {}".format(input))

        # check if text available
        if input.get('text', None):
            if Text.objects.filter(pk=from_global_id(input['text'])[1]).exists():
                text = Text.objects.get(pk=from_global_id(input['text'])[1])
            else:
                return cls(token=None, success=False, errors=["Text with ID {} not found".format(input['text'])])

        # create Token with transcription, transliteration, text, number and language
        token, token_obj = Token.objects.get_or_create(
            transcription=to_nfc(input['transcription']), transliteration=to_nfc(input['transliteration']), text=text, number=float(input['number']), language=input['language'])

        # get and add the lemmas
        for lemma in input['lemmas']:
            if Lemma.objects.filter(pk=from_global_id(lemma)[1]).exists():
                token.lemmas.add(Lemma.objects.get(pk=from_global_id(lemma)[1]))

       # get get and add the meanings
        for meaning in input['meanings']:
            if Meaning.objects.filter(pk=from_global_id(meaning)[1]).exists():
                token.meanings.add(Meaning.objects.get(pk=from_global_id(meaning)[1]))

        # get POS
        token.pos = input.get('pos')

       # morphological annotations
        for annotation in input['morphological_annotation']:
            annotation_obj, annotation_obj_created = MorphologicalAnnotation.objects.get_or_create(
                feature=annotation['feature'], feature_value=annotation['feature_value'])
            token.morphological_annotation.add(annotation_obj)

        # syntactic annotations
        for annotation in input['syntactic_annotation']:
            dep_obj, dep_created = Dependency.objects.get_or_create(head=annotation['head'], rel=annotation['rel'])
            token.syntactic_annotation.add(dep_obj)

        # check if comment available
        if input.get('comment', None):
            token.comment = to_nfc(input['comment'])

        # get or create uncertain
        for uncertain in input['uncertain']:
            uncertain_obj, uncertain_obj_created = CommentCategory.objects.get_or_create(
                category=uncertain)
            token.uncertain.add(uncertain_obj)

        # get or create to_discuss
        for to_discuss in input['to_discuss']:
            to_discuss_obj, to_discuss_obj_created = CommentCategory.objects.get_or_create(
                category=to_discuss)
            token.to_discuss.add(to_discuss_obj)

        # get or create new_suggestion
        for new_suggestion in input['new_suggestion']:
            new_suggestion_obj, new_suggestion_obj_created = CommentCategory.objects.get_or_create(
                category=new_suggestion)
            token.new_suggestion.add(new_suggestion_obj)

        # check if avestan available
        if input.get('avestan', None):
            token.avestan = to_nfc(input['avestan'])

        # check if previous token available
        if input.get('previous', None):
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                token.previous = Token.objects.get(pk=from_global_id(input['previous'])[1])
            else:
                return cls(token=None, success=False, errors=["Previous token with ID {} not found".format(input['previous'])])

        # check if line available
        if input.get('line', None):
            # check if line with assigned id already exists
            if Line.objects.filter(pk=from_global_id(input['line'])[1]).exists():
                line = Line.objects.get(pk=from_global_id(input['line'])[1])
                token.line = line
            else:
                return cls(token=None, success=False, errors=["Line with ID {} not found".format(input['line'])])

        # check if position_in_line available
        if input.get('position_in_line', None):
            position_in_line = input['position_in_line']
            token.position_in_line = position_in_line

        token.save()

        return cls(token=token, success=True, errors=None)


class UpdateToken(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        text = ID(required=True)
        transcription = String(required=True)
        transliteration = String(required=True)
        number = Float(required=True)
        language = Language(required=True)
        lemmas = List(ID, required=True)
        meanings = List(ID, required=True)
        pos = POS(required=False)
        morphological_annotation = List(MorphologicalAnnotationInput, required=True)
        syntactic_annotation = List(DependencyInput, required=True)
        comment = String(required=False)
        uncertain = List(String, required=True)
        to_discuss = List(String, required=True)
        new_suggestion = List(String, required=True)
        avestan = String(required=False)
        previous = ID(required=False)
        line = ID(required=False)
        position_in_line = Int(required=False)

    token = Field(TokenNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        # check if token with assigned id already exists
        if Token.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            # get the token
            token = Token.objects.get(pk=from_global_id(input['id'])[1])
        else:
            return cls(token=None, success=False, errors=["Token with ID {} not found".format(input['id'])])

        # update transcription
        token.transcription = to_nfc(input['transcription'])
        # update transliteration
        token.transliteration = to_nfc(input['transliteration'])
        # update language
        token.language = input.get('language')
        # update number
        token.number = float(input.get('number'))

        # get and add the lemmas
        for lemma in input['lemmas']:
            if Lemma.objects.filter(pk=from_global_id(lemma)[1]).exists():
                token.lemmas.add(Lemma.objects.get(pk=from_global_id(lemma)[1]))

       # get get and add the meanings
        for meaning in input['meanings']:
            if Meaning.objects.filter(pk=from_global_id(meaning)[1]).exists():
                token.meanings.add(Meaning.objects.get(pk=from_global_id(meaning)[1]))

        # set POS
        token.pos = input.get('pos')

       # morphological annotations
        token.morphological_annotation.clear()
        for annotation in input['morphological_annotation']:
            annotation_obj, annotation_obj_created = MorphologicalAnnotation.objects.get_or_create(
                feature=annotation['feature'], feature_value=annotation['feature_value'])
            token.morphological_annotation.add(annotation_obj)

        # syntactic annotations
        if input.get('syntactic_annotation'):
            token.syntactic_annotation.clear()
            for annotation in input['syntactic_annotation']:
                dep_obj, dep_created = Dependency.objects.get_or_create(head=annotation['head'], rel=annotation['rel'])
                token.syntactic_annotation.add(dep_obj)

        # check if comment available
        if input.get('comment', None):
            token.comment = to_nfc(input['comment'])

        # clear uncertain
        token.uncertain.clear()
        # get or create uncertain
        for uncertain in input['uncertain']:
            uncertain_obj, uncertain_obj_created = CommentCategory.objects.get_or_create(
                category=uncertain)
            token.uncertain.add(uncertain_obj)

        # clear to_discuss
        token.to_discuss.clear()
        # get or create to_discuss
        for to_discuss in input['to_discuss']:
            to_discuss_obj, to_discuss_obj_created = CommentCategory.objects.get_or_create(
                category=to_discuss)
            token.to_discuss.add(to_discuss_obj)

        # clear new_suggestion
        token.new_suggestion.clear()
        # get or create new_suggestion
        for new_suggestion in input['new_suggestion']:
            new_suggestion_obj, new_suggestion_obj_created = CommentCategory.objects.get_or_create(
                category=new_suggestion)
            token.new_suggestion.add(new_suggestion_obj)

        # check if avestan available
        if input.get('avestan', None):
            token.avestan = to_nfc(input['avestan'])

        # check if previous token available
        if input.get('previous', None):
            # check if previous token with assigned id already exists
            if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
                token.previous = Token.objects.get(pk=from_global_id(input['previous'])[1])
            else:
                return cls(token=None, success=False, errors=["Previous token with ID {} not found".format(input['previous'])])

           # check if line available
        if input.get('line', None):
            # check if line with assigned id already exists
            if Line.objects.filter(pk=from_global_id(input['line'])[1]).exists():
                line = Line.objects.get(pk=from_global_id(input['line'])[1])
                token.line = line
            else:
                return cls(token=None, success=False, errors=["Line with ID {} not found".format(input['line'])])

        # check if position_in_line available
        if input.get('position_in_line', None):
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
    @login_required
    def mutate_and_get_payload(cls, root, info, id):
        if Token.objects.filter(pk=from_global_id(id)[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(id)[1])
            token_instance.delete()
            return cls(success=True)

        else:
            return cls(success=False)


class AddLemmasToToken(relay.ClientIDMutation):
    class Input:
        token_id = ID(required=True)
        lemmas_ids = List(ID, required=True)

    success = Boolean()
    errors = List(String)

    token = Field(TokenNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("TOKEN_ID: {}, LEMMAS_ID: {}".format(input.get('token_id'), input.get('lemmas_ids')))

        if Token.objects.filter(pk=from_global_id(input['token_id'])[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(input.get('token_id'))[1])
            for lemma_id in input.get('lemmas_ids'):
                if Lemma.objects.filter(pk=from_global_id(lemma_id)[1]).exists():
                    lemma_instance = Lemma.objects.get(pk=from_global_id(lemma_id)[1])
                    token_instance.lemmas.add(lemma_instance)

                else:
                    return cls(success=False, errors=["Lemma with ID {} not found".format(lemma_id)], token=None)

            token_instance.save()
            return cls(token=token_instance, success=True, errors=None)
        else:
            return cls(token=None, success=False, errors=["Token with ID {} not found".format(input.get('token_id'))])


class AddMeaningsToToken(relay.ClientIDMutation):
    class Input:
        token_id = ID(required=True)
        meanings_ids = List(ID, required=True)

    success = Boolean()
    errors = List(String)

    token = Field(TokenNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("TOKEN_ID: {}, MEANINGS_ID: {}".format(input.get('token_id'), input.get('meanings_ids')))

        if Token.objects.filter(pk=from_global_id(input['token_id'])[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(input.get('token_id'))[1])
            for meaning_id in input.get('meanings_ids'):
                if Meaning.objects.filter(pk=from_global_id(meaning_id)[1]).exists():
                    meaning_instance = Meaning.objects.get(pk=from_global_id(meaning_id)[1])
                    token_instance.meanings.add(meaning_instance)

                else:
                    return cls(success=False, errors=["Meaning with ID {} not found".format(meaning_id)], token=None)

            token_instance.save()
            return cls(token=token_instance, success=True, errors=None)
        else:
            return cls(token=None, success=False, errors=["Token with ID {} not found".format(input.get('token_id'))])


class RemoveLemmasFromToken(relay.ClientIDMutation):
    class Input:
        token_id = ID(required=True)
        lemmas_ids = List(ID, required=True)

    success = Boolean()
    errors = List(String)

    token = Field(TokenNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("TOKEN_ID: {}, LEMMAS_ID: {}".format(input.get('token_id'), input.get('lemmas_ids')))

        if Token.objects.filter(pk=from_global_id(input['token_id'])[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(input.get('token_id'))[1])
            for lemma_id in input.get('lemmas_ids'):
                if Lemma.objects.filter(pk=from_global_id(lemma_id)[1]).exists():
                    lemma_instance = Lemma.objects.get(pk=from_global_id(lemma_id)[1])
                    token_instance.lemmas.remove(lemma_instance)

                else:
                    return cls(success=False, errors=["Lemma with ID {} not found".format(lemma_id)], token=None)

            token_instance.save()
            return cls(token=token_instance, success=True, errors=None)
        else:
            return cls(token=None, success=False, errors=["Token with ID {} not found".format(input.get('token_id'))])


class RemoveMeaningsFromToken(relay.ClientIDMutation):
    class Input:
        token_id = ID(required=True)
        meanings_ids = List(ID, required=True)

    success = Boolean()
    errors = List(String)

    token = Field(TokenNode)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        logger.error("TOKEN_ID: {}, MEANINGS_ID: {}".format(input.get('token_id'), input.get('meanings_ids')))

        if Token.objects.filter(pk=from_global_id(input['token_id'])[1]).exists():
            token_instance = Token.objects.get(pk=from_global_id(input.get('token_id'))[1])
            for meaning_id in input.get('meanings_ids'):
                if Meaning.objects.filter(pk=from_global_id(meaning_id)[1]).exists():
                    meaning_instance = Meaning.objects.get(pk=from_global_id(meaning_id)[1])
                    token_instance.meanings.remove(meaning_instance)

                else:
                    return cls(success=False, errors=["Meaning with ID {} not found".format(meaning_id)], token=None)

            token_instance.save()
            return cls(token=token_instance, success=True, errors=None)
        else:
            return cls(token=None, success=False, errors=["Token with ID {} not found".format(input.get('token_id'))])


class JoinTokens(relay.ClientIDMutation):
    class Input():
        current = ID(required=True)
        previous = ID(required=True)

    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # get token

        if Token.objects.filter(pk=from_global_id(input['current'])[1]).exists():
            current_token = Token.objects.get(pk=from_global_id(input['current'])[1])
        else:
            return cls(success=False, errors=["Token with ID {} not found".format(input['current'])])
        logger.error("TOKEN_ID: {}".format(current_token.id))

        # get previous token
        if Token.objects.filter(pk=from_global_id(input['previous'])[1]).exists():
            previous_token = Token.objects.get(pk=from_global_id(input['previous'])[1])
            current_token.previous = previous_token
            previous_token.save()
        else:
            return cls(success=False, errors=["Token with ID {} not found".format(input['previous'])])

        return cls(success=True)


class Mutation(ObjectType):
    add_lemmas_to_token = AddLemmasToToken.Field()
    add_meanings_to_token = AddMeaningsToToken.Field()
    remove_lemmas_from_token = RemoveLemmasFromToken.Field()
    remove_meanings_from_token = RemoveMeaningsFromToken.Field()
    create_token = CreateToken.Field()
    delete_token = DeleteToken.Field()
    update_token = UpdateToken.Field()
    join_tokens = JoinTokens.Field()
