from typing import Optional, List, cast
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

from mpcd.dict.types.meaning import MeaningInput
from mpcd.dict.types.lemma import LemmaInput

from mpcd.corpus.types.token import Token, TokenInput, TokenPartial
from mpcd.corpus.types.token_comment import TokenCommentInput
import mpcd.corpus.models as corpus_models
import mpcd.dict.models as dict_models


@gql.type
class Query:
    token: Optional[Token] = gql.django.node()
    tokens: relay.Connection[Token] = gql.django.connection()


@gql.type
class Mutation:

    create_token: Token = gql.django.create_mutation(TokenInput)
    update_token: Token = gql.django.update_mutation(TokenPartial)
    delete_token: Token = gql.django.delete_mutation(gql.NodeInput)

    @gql.django.input_mutation
    def join_tokens(self, info,
                    current: relay.GlobalID,
                    previous: relay.GlobalID,
                    ) -> Token:

        current_token = current.resolve_node(info)
        previous_token = previous.resolve_node(info)
        current_token.previous = previous_token
        current_token.save()
        return current_token

    @gql.django.input_mutation
    def add_lemmas_to_token(self, info,
                            token: relay.GlobalID,
                            lemmas: List[relay.GlobalID],
                            ) -> Token:

        token = token.resolve_node(info)
        lemmas = [lemma.resolve_node(info) for lemma in lemmas]
        token.lemmas.add(*lemmas)
        token.save()
        return token

    @gql.django.input_mutation
    def add_new_lemma_to_token(self, info,
                            token: relay.GlobalID,
                            lemma: LemmaInput,
                            ) -> Token:

        token = token.resolve_node(info)
        lemma = dict_models.Lemma.objects.create(**lemma)
        token.lemmas.add(lemma)
        token.save()
        return token

    @gql.django.input_mutation
    def add_meanings_to_token(self, info,
                              token: relay.GlobalID,
                              meanings: List[relay.GlobalID],
                              ) -> Token:

        token = token.resolve_node(info)
        meanings = [meaning.resolve_node(info) for meaning in meanings]
        token.meanings.add(*meanings)
        token.save()
        return token

    @gql.django.input_mutation
    def add_new_meaning_to_token(self, info,
                              token: relay.GlobalID,
                              meaning: MeaningInput,
                              ) -> Token:

        token = token.resolve_node(info)
        meaning = dict_models.Meaning.objects.create(**meaning)
        token.meanings.add(meaning)
        token.save()
        return token

    @gql.django.input_mutation
    def remove_lemmas_from_token(self,
                                 info,
                                 token: relay.GlobalID,
                                 lemmas: List[relay.GlobalID],
                                 ) -> Token:

        token = token.resolve_node(info)
        lemmas = [lemma.resolve_node(info) for lemma in lemmas]
        token.lemmas.remove(*lemmas)
        token.save()
        return token

    @gql.django.input_mutation
    def add_tokens_comment_to_token(self,
                                   info,
                                   token: relay.GlobalID,
                                   token_comments: List[relay.GlobalID],
                                   ) -> Token:

        token = token.resolve_node(info)
        token_comments = [token_comment.resolve_node(info) for token_comment in token_comments]
        token.comments.add(*token_comments)
        token.save()
        return token

    @gql.django.input_mutation
    def add_new_token_comment_to_token(self,
                                   info,
                                   token: relay.GlobalID,
                                   token_comment: TokenCommentInput,
                                   ) -> Token:

        token = token.resolve_node(info)
        token_comment = corpus_models.TokenComment.objects.create(**token_comment)
        token.comments.add(token_comment)
        token.save()
        return token

schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])
