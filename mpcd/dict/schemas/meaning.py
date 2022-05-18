from click import command
from graphene import relay, InputObjectType, String, Field, ObjectType, ID, Boolean, List
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import graphene_django_optimizer as gql_optimizer
from graphql_jwt.decorators import login_required

from mpcd.dict.models import Meaning
from mpcd.utils.normalize import to_nfc


class MeaningNode(DjangoObjectType):
    class Meta:
        model = Meaning
        filter_fields = {'meaning': ['exact', 'icontains', 'istartswith'],
                         'language': ['exact', 'icontains', 'istartswith'],
                         'comment': ['icontains', 'istartswith']}
        interfaces = (relay.Node,)


class MeaningInput(InputObjectType):
    meaning = String(required=True)
    language = String(required=True)
    related_meanings = List(ID, required=True)
    comment = String(required=False)


# Queries
class Query(ObjectType):
    meaning = relay.Node.Field(MeaningNode)
    all_meanings = DjangoFilterConnectionField(MeaningNode)

    @login_required
    def resolve_all_meanings(self, info, **kwargs):
        return gql_optimizer.query(Meaning.objects.all(), info)


class CreateMeaning(relay.ClientIDMutation):
    class Input:
        meaning = String(required=True)
        language = String(required=True)
        related_meanings = List(ID, required=True)
        comment = String(required=False)

    meaning = Field(MeaningNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        meaning, meaning_created = Meaning.objects.get_or_create(
            meaning=to_nfc(input.get('meaning')), language=to_nfc(input.get('language')))

        for related_meaning in input.get('related_meanings'):
            meaning_rel, meaning_rel_created = Meaning.objects.get(id=from_global_id(related_meaning.get('id'))[1])
            meaning.related_meanings.add(meaning_rel)

        if input.get('comment'):
            meaning.comment = input.get('comment')

        meaning.save()

        return cls(meaning=meaning, success=True)


class UpdateMeaning(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
        meaning = String(required=True)
        language = String(required=True)

    errors = List(String)
    word = Field(MeaningNode)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Meaning.objects.filter(id=from_global_id(input.get('id'))[1]).exists():
            meaning = Meaning.objects.get(id=from_global_id(input.get('id'))[1])
            meaning.meaning = to_nfc(input.get('meaning'))
            meaning.language = to_nfc(input.get('language'))
            meaning.comment = input.get('comment')
            if input.get('related_meanings'):
                meaning.related_meanings.clear()
                for related_meaning in input.get('related_meanings'):
                    meaning_rel, meaning_rel_created = Meaning.objects.get(
                        id=from_global_id(related_meaning.get('id'))[1])
                    meaning.related_meanings.add(meaning_rel)
            meaning.save()
            return cls(meaning=meaning, success=True)
        else:
            return cls(errors=['Meaning ID does not exist'], success=False)


class DeleteMeaning(relay.ClientIDMutation):
    class Input:
        id = ID(required=True)
    success = Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        if Meaning.objects.filter(id=from_global_id(input.get('id'))[1]).exists():
            Meaning.objects.get(id=from_global_id(input.get('id'))[1]).delete()
            return cls(success=True)
        else:
            return cls(success=False)


class Mutation(ObjectType):
    create_meaning = CreateMeaning.Field()
    update_meaning = UpdateMeaning.Field()
    delete_meaning = DeleteMeaning.Field()
