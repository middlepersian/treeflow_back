from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List

from mpcd.corpus.types.sentence import Sentence, SentenceInput, SentencePartial

from mpcd.dict.types.meaning import MeaningInput
from mpcd.corpus.types.token import TokenInput

import mpcd.corpus.models as corpus_models
import mpcd.dict.models as dict_models


from strawberry_django_plus.directives import SchemaDirectiveExtension

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


@gql.type
class Query:
    sentence: Optional[Sentence] = gql.django.node(directives=[IsAuthenticated()])
    sentences:  relay.Connection[Sentence] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:
    create_sentence: Sentence = gql.django.create_mutation(SentenceInput, directives=[IsAuthenticated()])
    update_sentence: Sentence = gql.django.update_mutation(SentencePartial, directives=[IsAuthenticated()])
    delete_sentence: Sentence = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.input_mutation
    def add_tokens_to_sentence(self,
                               info,
                               sentence: relay.GlobalID,
                               tokens: List[relay.GlobalID],
                               ) -> Sentence:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        tokens = [token.resolve_node(info) for token in tokens]
        sentence.tokens.set(tokens)
        sentence.save()
        return sentence

    @gql.django.input_mutation
    def add_new_token_to_sentence(self,
                                  info,
                                  sentence: relay.GlobalID,
                                  token: TokenInput,
                                  ) -> Sentence:

        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        data = vars(token)
        token = resolvers.create(info, corpus_models.Token, resolvers.parse_input(info, data))
        sentence.tokens.add(token)
        sentence.save()
        return sentence

    @gql.django.input_mutation
    def remove_tokens_from_sentence(self,
                                    info,
                                    sentence: relay.GlobalID,
                                    tokens: List[relay.GlobalID],
                                    ) -> Sentence:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        tokens = [token.resolve_node(info) for token in tokens]
        sentence.tokens.remove(*tokens)
        sentence.save()
        return sentence

    @gql.django.input_mutation
    def add_meanings_to_sentence(self,
                                 info,
                                 sentence: relay.GlobalID,
                                 meanings: List[relay.GlobalID],
                                 ) -> Sentence:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        meanings = [meaning.resolve_node(info) for meaning in meanings]
        sentence.meanings.add(*meanings)
        return sentence

    @gql.django.input_mutation
    def add_new_meaning_to_sentence(self,
                                    info,
                                    sentence: relay.GlobalID,
                                    meaning: MeaningInput,
                                    ) -> Sentence:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        data = vars(meaning)
        meaning = resolvers.create(info, dict_models.Meaning, resolvers.parse_input(info, data))
        sentence.meanings.add(meaning)
        return sentence

    @gql.django.input_mutation
    def remove_meanings_from_sentence(self,
                                      info,
                                      sentence: relay.GlobalID,
                                      meanings: List[relay.GlobalID],
                                      ) -> Sentence:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")

        sentence = sentence.resolve_node(info)
        meanings = [meaning.resolve_node(info) for meaning in meanings]
        sentence.meanings.remove(*meanings)
        return sentence


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
