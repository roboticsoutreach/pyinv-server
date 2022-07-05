"""
This file does nothing. It is a massive hack around a bug in djangorestframework-stubs!

https://github.com/typeddjango/djangorestframework-stubs/issues/230

The alternative is a lot of type:ignores in the tests, which is much more of a pain to remove afterwards.
"""

from typing import Any, Dict, Optional, Union

from rest_framework import response
from rest_framework.test import APIClient


class Response(response.Response):
    def json(self) -> Any:
        super().json()  # type: ignore


class TestClient(APIClient):
    def request(self, **kwargs) -> Response:  # type: ignore
        return super().request(**kwargs)  # type: ignore

    def get(  # type: ignore
        self,
        path: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        follow: bool = False,  # noqa: A002
        **extra: Any,
    ) -> Response:
        return super().get(path, data, follow, **extra)

    def post(  # type: ignore
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,  # noqa: A002
        content_type: Optional[str] = None,
        follow: bool = False,
        **extra: Any,
    ) -> Response:
        return super().post(path, data, format, content_type, follow, **extra)  # type: ignore

    def put(  # type: ignore
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,  # noqa: A002
        content_type: Optional[str] = None,
        follow: bool = False,
        **extra: Any,
    ) -> Response:
        return super().put(path, data, format, content_type, follow, **extra)  # type: ignore

    def patch(  # type: ignore
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,  # noqa: A002
        content_type: Optional[str] = None,
        follow: bool = False,
        **extra: Any,
    ) -> Response:
        return super().patch(path, data, format, content_type, follow, **extra)  # type: ignore

    def delete(  # type: ignore
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,  # noqa: A002
        content_type: Optional[str] = None,
        follow: bool = False,
        **extra: Any,
    ) -> Response:
        return super().delete(path, data, format, content_type, follow, **extra)  # type: ignore
