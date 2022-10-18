from strawberry_django_plus import gql
from strawberry_django_plus.mutations import resolvers
from strawberry_django_plus.gql import relay
from typing import List, TYPE_CHECKING, Optional
from strawberry.lazy_type import LazyType

from mpcd.corpus import models


@gql.django.type(models.SectionType)
class SectionType(relay.Node):
    section_section_type: relay.Connection[LazyType['Section', 'mpcd.corpus.types.section']]

    id: gql.auto
    identifier: gql.auto
