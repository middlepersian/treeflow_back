import unicodedata
from typing import Any, ClassVar, Callable
import strawberry
from strawberry.directive import DirectiveLocation
from strawberry_django_plus.directives import SchemaDirectiveWithResolver, SchemaDirectiveHelper
from strawberry.schema_directive import Location
from graphql.type.definition import GraphQLResolveInfo
from strawberry.utils.await_maybe import AwaitableOrValue
import unicodedata
from typing import Any, ClassVar, Callable
import dataclasses


@strawberry.directive(
        locations=[DirectiveLocation.FIELD], description="Normalize Unicode characters in the field value."
    )
def normalize(value: str, form: str ="NFC"):
    return unicodedata.normalize(form, value)


@strawberry.schema_directive(
    locations=[Location.FIELD_DEFINITION],
    description="Normalize Unicode characters in the field value."
)
@dataclasses.dataclass
class NormalizeDirective(SchemaDirectiveWithResolver):
    def __init__(self, form):
        self.form = form

    def resolve(self, helper: SchemaDirectiveHelper, next_resolver: Callable, root: Any, info: GraphQLResolveInfo, **kwargs):
        value = next_resolver(root, info, **kwargs)
        if isinstance(value, str):
            return unicodedata.normalize(self.form, value)
        elif isinstance(value, list):
            return [unicodedata.normalize(self.form, x) if isinstance(x, str) else x for x in value]
        else:
            return value


        
