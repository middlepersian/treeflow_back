from typing import Dict, Tuple, Type, Union, cast

from django.test.client import AsyncClient  # type:ignore
from django.test.client import Client
import pytest

from strawberry_django_plus.optimizer import DjangoOptimizerExtension
from .utils import GraphQLTestClient


@pytest.fixture(params=["async", "async_no_optimizer"])
def gql_client(request):
    client, path, with_optimizer = cast(
        Dict[str, Tuple[Union[Type[Client], Type[AsyncClient]], str, bool]],
        {
            "async": (AsyncClient, "/graphql/", True),
            "async_no_optimizer": (AsyncClient, "/graphql/", False),
        },
    )[request.param]
    token = DjangoOptimizerExtension.enabled.set(with_optimizer)
    with GraphQLTestClient(path, client()) as c:
        yield c
    DjangoOptimizerExtension.enabled.reset(token)
