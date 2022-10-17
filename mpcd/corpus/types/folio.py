from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from strawberry.lazy_type import LazyType
from typing import List, TYPE_CHECKING, Optional
from mpcd.corpus import models



@gql.django.type(models.Folio)
class Folio(relay.Node):

    line_folio: relay.Connection[LazyType['Line', 'mpcd.corpus.types.line']]  
      
    id: gql.auto
    number: gql.auto
    facsimile: LazyType['Facsimile', 'mpcd.corpus.types.facsimile']
    comments: List[LazyType['Comment', 'mpcd.corpus.types.comment']]
    previous: Optional['Folio']


    