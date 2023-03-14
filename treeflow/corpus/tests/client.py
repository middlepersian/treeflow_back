import contextlib
from typing import Any, Awaitable, Dict, Optional, cast, Union, overload

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractUser
from django.test.client import AsyncClient, Client  # type:ignore
from strawberry.test import BaseGraphQLTestClient
from strawberry.test.client import Response

from strawberry_django_plus.test.client import TestClient

class GraphQLTestClient(TestClient):
    def __init__(
        self,
        path: str,
        client: Union[Client, AsyncClient],
    ):
        super().__init__(path, client=client)
        self._token: Optional[contextvars.Token] = None
        self.is_async = isinstance(client, AsyncClient)

    def __enter__(self):
        self._token = _client.set(self)
        return self

    def __exit__(self, *args, **kwargs):
        assert self._token
        _client.reset(self._token)

    def request(
        self,
        body: Dict[str, object],
        headers: Optional[Dict[str, object]] = None,
        files: Optional[Dict[str, object]] = None,
    ):
        kwargs: Dict[str, object] = {"data": body}
        if files:  # pragma:nocover
            kwargs["format"] = "multipart"
        else:
            kwargs["content_type"] = "application/json"

        return self.client.post(self.path, **kwargs)

    def query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, object]] = None,
        asserts_errors: Optional[bool] = True,
        files: Optional[Dict[str, object]] = None,
    ) -> Response:
        body = self._build_body(query, variables, files)

        resp = self.request(body, headers, files)
        if inspect.iscoroutine(resp):
            resp = asyncio.run(resp)

        data = self._decode(resp, type="multipart" if files else "json")

        response = Response(
            errors=data.get("errors"),
            data=data.get("data"),
            extensions=data.get("extensions"),
        )
        if asserts_errors:
            assert response.errors is None

        return response