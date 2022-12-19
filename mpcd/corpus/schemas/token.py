from typing import Optional, List, cast
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.mutations import resolvers

from mpcd.dict.types.meaning import MeaningInput
from mpcd.dict.types.lemma import LemmaInput

from mpcd.corpus import models as corpus_models
from mpcd.dict import models as dict_models

from mpcd.corpus.types.token import Token, TokenInput, TokenPartial
from mpcd.corpus.types.token_comment import TokenCommentInput

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
    token: Optional[Token] = gql.django.node(directives=[IsAuthenticated()])
    tokens: relay.Connection[Token] = gql.django.connection(directives=[IsAuthenticated()])


@gql.type
class Mutation:

    create_token: Token = gql.django.create_mutation(TokenInput, directives=[IsAuthenticated()])
    update_token: Token = gql.django.update_mutation(TokenPartial, directives=[IsAuthenticated()])
    delete_token: Token = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.input_mutation
    def join_tokens(self, info,
                    current: relay.GlobalID,
                    previous: relay.GlobalID,
                    ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
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
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
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
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node(info)
        data = vars(lemma)
        lemma = resolvers.create(info, dict_models.Lemma, resolvers.parse_input(info, data))
        token.lemmas.add(lemma)
        token.save()
        return token

    @gql.django.input_mutation
    def add_meanings_to_token(self, info,
                              token: relay.GlobalID,
                              meanings: List[relay.GlobalID],
                              ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
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
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node(info)
        data = vars(meaning)
        meaning = resolvers.create(info, dict_models.Meaning, resolvers.parse_input(info, data))
        token.meanings.add(meaning)
        token.save()
        return token

    @gql.django.input_mutation
    def remove_lemmas_from_token(self,
                                 info,
                                 token: relay.GlobalID,
                                 lemmas: List[relay.GlobalID],
                                 ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
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
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
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
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node(info)
        data = vars(token_comment)
        token_comment = resolvers.create(info, corpus_models.TokenComment, resolvers.parse_input(info, data))
        token.comments.add(token_comment)
        token.save()
        return token


schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])
