"""The lokate service of an arkitekt app.

lokate has no structures: points, visits, trips and places are addressed by the phone's
own client ids, never sent between actions by id. An app takes the service in with
``App(services=[lokate_service])``.
"""

import os
from typing import Annotated

from fakts import Alias, Require, TokenLoader
from fakts.contrib.rath.auth import FaktsAuthLink
from rath.links.aiohttp import AIOHttpLink
from rath.links.compose import compose
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.split import SplitLink
from rekuest.app import AppRegistry

from graphql import OperationType
from lokate.lokate import Lokate
from lokate.rath import LokateRath


def build_relative_path(*path: str) -> str:
    """Build a path relative to this file, for the files shipped beside it."""
    return os.path.join(os.path.dirname(__file__), *path)


registry = AppRegistry()
"""What lokate brings to an app: its service."""


@registry.service(
    schema=build_relative_path("api", "schema.graphql"),
    turms=build_relative_path("api", "project.json"),
)
def lokate(
    lokate: Annotated[
        Alias,
        Require(
            "live.arkitekt.lokate",
            "Where the backed-up location timeline is kept",
        ),
    ],
    tokens: TokenLoader,
) -> Lokate:
    """Lokate: the server copy of your phones' location timeline."""
    return Lokate(
        rath=LokateRath(
            link=compose(
                FaktsAuthLink(token_loader=tokens),
                SplitLink(
                    left=AIOHttpLink(
                        endpoint_url=lokate.to_http_path("graphql"),
                        proxy=lokate.proxy,
                    ),
                    right=GraphQLWSLink(
                        ws_endpoint_url=lokate.to_ws_path("graphql"),
                        proxy=lokate.proxy,
                    ),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        ),
    )
