from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required


from mpcd.dict.models import Semantic
from mpcd.dict.models import Meaning
from mpcd.dict.models import TermTech
from mpcd.dict.models import Lemma
from mpcd.dict.schemas import MeaningInput
from mpcd.dict.schemas import LemmaInput
from mpcd.dict.schemas import TermTechInput


from mpcd.utils.normalize import to_nfc


class SemanticNode(DjangoObjectType):
    class Meta:
        model = Semantic
        filter_fields = {
            'comment': ['exact', 'icontains', 'istartswith']}
        interfaces = (relay.Node,)


class SemanticInput(InputObjectType):
    lemmas = List(LemmaInput, required=True)
    meanings = List(MeaningInput, required=True)
    term_techs = List(TermTechInput, required=True)
    comment = String(required=False)

# Queries


class Query(ObjectType):
    semantic = relay.Node.Field(SemanticNode)
    all_semantics = DjangoFilterConnectionField(SemanticNode)

    @ login_required
    def resolve_all_semantics(self, info, **kwargs):
        return gql_optimizer.query(Semantic.objects.all(), info)

# Mutations


class CreateSemantic(relay.ClientIDMutation):
    class Input:
        lemmas = List(LemmaInput, required=True)
        meanings = List(MeaningInput, required=True)
        term_techs = List(TermTechInput, required=True)
        comment = String(required=False)

    semantic = Field(SemanticNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):

        # create semantic
        semantic = Semantic()

        # Lemmas
        for lemma in input['lemmas']:
            lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(
                input.get('word')), language=to_nfc(input.get('language')))
            semantic.lemmas.add(lemma)

        # Meanings
        for meaning_input in input['meanings']:
            meaning_obj, meaning_created = Meaning.objects.get_or_create(
                meaning=to_nfc(meaning_input['meaning']), language=meaning_input['language'])
            semantic.meanings.add(lemma)

        # TermTechs
        for term_tech_input in input['term_techs']:
            term_tech_obj, term_tech_created = TermTech.objects.get_or_create(category=term_tech_input['category'])
            semantic.term_techs.add(term_tech_obj)

        # Comment
        if input('comment', None):
            semantic.comment = input['comment']

        semantic.save()
        return cls(semantic=semantic, success=True, errors=None)


class UpdateSemantic(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        lemmas = List(LemmaInput, required=True)
        meanings = List(MeaningInput, required=True)
        term_techs = List(TermTechInput, required=True)
        comment = String(required=False)

    semantic = Field(SemanticNode)
    success = Boolean()
    errors = List(String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Semantic.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            semantic_obj = Semantic.objects.get(pk=from_global_id(input['id'])[1])
        else:
            return cls(success=False, errors=['Semantic ID does not exist'])
        # Lemmas
        # clear all lemmas
        semantic_obj.lemmas.clear()
        for lemma in input['lemmas']:
            lemma, lemma_created = Lemma.objects.get_or_create(word=to_nfc(
                input.get('word')), language=to_nfc(input.get('language')))
            semantic_obj.lemmas.add(lemma)

        # Meanings
        # clear all meanings
        semantic_obj.meanings.clear()
        for meaning_input in input['meanings']:
            meaning_obj, meaning_created = Meaning.objects.get_or_create(
                meaning=to_nfc(meaning_input['meaning']), language=meaning_input['language'])
            if meaning_obj:
                semantic_obj.meanings.add(meaning_obj)
        # TermTechs
        # clear all term_techs
        semantic_obj.term_techs.clear()
        for term_tech_input in input['term_techs']:
            term_tech_obj, term_tech_created = TermTech.objects.get_or_create(category=term_tech_input['category'])
            if term_tech_obj:
                semantic_obj.term_techs.add(term_tech_obj)
        # Comment
        if input('comment', None):
            semantic_obj.comment = input['comment']

        semantic_obj.save()
        return cls(semantic=semantic_obj, success=True, errors=None)


class DeleteSemantic(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)

    success = Boolean()
    errors = List(String)

    def mutate_and_get_payload(cls, root, info, **input):
        if Semantic.objects.filter(pk=from_global_id(input['id'])[1]).exists():
            semantic_obj = Semantic.objects.get(pk=from_global_id(input['id'])[1])
            semantic_obj.delete()
            return cls(success=True)
        else:
            return cls(success=False, errors=['Semantic ID does not exist'])


class Mutation(ObjectType):
    create_semantic = CreateSemantic.Field()
    update_semantic = UpdateSemantic.Field()
    delete_semantic = DeleteSemantic.Field()
