from strawberry_django_plus import gql
from strawberry_django_plus.gql import relay
from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from strawberry_django_plus.mutations import resolvers

from typing import Optional

from treeflow.corpus.types.source import Source, SourceInput, SourcePartial
from treeflow.corpus.types.bibliography import BibEntry, BibEntryInput, BibEntryPartial
from treeflow.corpus.models.source import Source as SourceModel
from treeflow.corpus.models.bibliography import BibEntry as BibEntryModel


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
    source: Optional[Source] = gql.django.node()
    sources:  relay.Connection[Source] = gql.django.connection()


@gql.type
class Mutation:
    create_source: Source = gql.django.create_mutation(SourceInput, directives=[IsAuthenticated()])
    update_source: Source = gql.django.update_mutation(SourcePartial, directives=[IsAuthenticated()])
    delete_source: Source = gql.django.delete_mutation(gql.NodeInput, directives=[IsAuthenticated()])

    @gql.django.mutation
    def create_source_with_new_bibentry(self, info, source: SourceInput, bibentry: BibEntryInput) -> Source:
        if not info.context or not info.context.request.user.is_authenticated:
            raise Exception("Not authenticated")
        source =  vars(source)
        bibentry = vars(bibentry)
        #create bibentry
        new_bibentry = resolvers.create(info, BibEntryModel, resolvers.parse_input(info, bibentry))
        new_bibentry.save()
        #create source
        new_source = resolvers.create(info, SourceModel, resolvers.parse_input(info, source))
        # add bibentry to source
        new_source.references.add(new_bibentry)
        new_source.save()
        return new_source   
schema = gql.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension, SchemaDirectiveExtension])




