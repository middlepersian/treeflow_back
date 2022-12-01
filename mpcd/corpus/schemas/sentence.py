from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from typing import Optional, List

from mpcd.corpus.types.sentence import Sentence, SentenceInput, SentencePartial

from mpcd.dict.types.meaning import  MeaningInput
from mpcd.corpus.types.token import  TokenInput

import mpcd.corpus.models as corpus_models
import mpcd.dict.models as dict_models

@gql.type
class Query:
    sentence: Optional[Sentence] = gql.django.node()
    sentences:  relay.Connection[Sentence] = gql.django.connection()


@gql.type
class Mutation:
    create_sentence: Sentence = gql.django.create_mutation(SentenceInput)
    update_sentence: Sentence = gql.django.update_mutation(SentencePartial)
    delete_sentence: Sentence = gql.django.delete_mutation(gql.NodeInput)

    @gql.django.input_mutation
    def add_tokens_to_sentence(self,
                               info,
                               sentence: relay.GlobalID,
                               tokens: List[relay.GlobalID],
                               ) -> Sentence:

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

        sentence = sentence.resolve_node(info)
        token = corpus_models.Token.objects.create(**token)
        sentence.tokens.add(token)
        sentence.save()
        return sentence

    @gql.django.input_mutation
    def remove_tokens_from_sentence(self,
                                    info,
                                    sentence: relay.GlobalID,
                                    tokens: List[relay.GlobalID],
                                    ) -> Sentence:

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

        sentence = sentence.resolve_node(info)
        meaning = dict_models.Meaning.objects.create(**meaning)
        sentence.meanings.add(meaning)
        return sentence

    @gql.django.input_mutation
    def remove_meanings_from_sentence(self,
                                      info,
                                      sentence: relay.GlobalID,
                                      meanings: List[relay.GlobalID],
                                      ) -> Sentence:

        sentence = sentence.resolve_node(info)
        meanings = [meaning.resolve_node(info) for meaning in meanings]
        sentence.meanings.remove(*meanings)
        return sentence


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
