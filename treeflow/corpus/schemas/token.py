from asgiref.sync import sync_to_async
from typing import Optional, List
from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.mutations import resolvers

from treeflow.dict.types.meaning import MeaningInput
from treeflow.dict.types.lemma import LemmaInput
from treeflow.corpus.documents.token import TokenDocument

from treeflow.corpus import models as corpus_models
from treeflow.dict import models as dict_models

from treeflow.corpus.types.token import Token, TokenInput, TokenPartial, TokenElastic
from treeflow.corpus.types.dependency import DependencyInput

from strawberry_django_plus.directives import SchemaDirectiveExtension

from treeflow.corpus.directives.normalization import normalize

from strawberry_django_plus.permissions import (
    HasObjPerm,
    HasPerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)


from elasticsearch_dsl import Search, Q, connections
es_conn = connections.create_connection(hosts=['elastic:9200'], timeout=20)


@gql.type
class Query:
    token: Optional[Token] = gql.django.node(directives=[IsAuthenticated()])
    tokens: relay.Connection[Token] = gql.django.connection(directives=[IsAuthenticated()])

    @gql.field
    @sync_to_async
    def search_tokens(pattern: str, query_type: str, size: int = 100) -> List[TokenElastic]:

        q = Q(query_type, transcription=pattern)
        response = TokenDocument.search().query(q).extra(size=size)

        tokens = []
        for hit in response:
            token = TokenElastic.from_hit(hit)
            tokens.append(token)

        return tokens
    
    
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
    def add_new_dependency_to_token(self, info,
                                    token: relay.GlobalID,
                                    dependency: DependencyInput,
                                    ) -> Token:
        if not info.context.request.user.is_authenticated:
            raise Exception("You must be authenticated for this operation.")
        token = token.resolve_node(info)
        dependency = resolvers.create(info, corpus_models.Dependency, resolvers.parse_input(info, data))
        token.dependencies.add(dependency)
        token.save()
        return token
    



schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension], directives=[normalize])
