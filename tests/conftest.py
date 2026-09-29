import os
import socket
import sys
from collections.abc import Generator
from dataclasses import dataclass

import pytest
from dokker import Deployment, testing
from dokker.log_watcher import LogWatcher
from rath.links.aiohttp import AIOHttpLink
from rath.links.auth import ComposedAuthLink
from rath.links.compose import compose
from rath.links.graphql_ws import GraphQLWSLink
from rath.links.timeout import TimeoutLink

from graphql import OperationType
from lokate.lokate import Lokate
from lokate.rath import (
    LokateRath,
    SplitLink,
)


def pytest_configure(config: pytest.Config) -> None:
    """Register custom platform markers."""
    config.addinivalue_line("markers", "linux_only: skip on non-Linux platforms")
    config.addinivalue_line("markers", "no_windows: skip on Windows")


def pytest_collection_modifyitems(config: pytest.Config, items: list) -> None:
    """Skip tests marked linux_only or no_windows on the wrong platform."""
    for item in items:
        if item.get_closest_marker("linux_only") and sys.platform != "linux":
            item.add_marker(pytest.mark.skip(reason="Linux only"))
        if item.get_closest_marker("no_windows") and sys.platform == "win32":
            item.add_marker(pytest.mark.skip(reason="Not supported on Windows"))


project_path = os.path.join(os.path.dirname(__file__), "integration")
docker_compose_file = os.path.join(project_path, "docker-compose.yml")
#: Optional, gitignored: mounts a local lokate-server checkout over the image's
#: /workspace, so the suite can test server changes that are not published yet.
#: See tests/integration/docker-compose.local.yml.
local_override_file = os.path.join(project_path, "docker-compose.local.yml")
compose_files = [docker_compose_file] + (
    [local_override_file] if os.path.exists(local_override_file) else []
)


def _reserve_free_ports(count: int) -> list[int]:
    """Ask the OS for `count` distinct free TCP ports.

    All sockets are held open until every port has been assigned, so the kernel
    cannot hand out the same port twice within one call. They are released
    before compose binds them -- a race in theory, but the ephemeral range is
    large and this is what keeps concurrent runs (and the leftovers of a crashed
    one) from colliding on a fixed port.
    """
    sockets: list[socket.socket] = []
    try:
        for _ in range(count):
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            sockets.append(sock)
        return [int(sock.getsockname()[1]) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


@pytest.fixture(scope="session")
def integration_ports() -> Generator[dict[str, int], None, None]:
    """Pick this run's host ports and point compose at them.

    Reserved rather than left to docker (`ports: - "80"`) because
    `Deployment.spec` is rendered by `docker compose config`, which is static:
    an unpublished port reads back as ``None`` and the test URLs would quietly
    become ``http://localhost:None`` instead of failing loudly.
    """
    (lokate_port,) = _reserve_free_ports(1)
    env = {"LOKATE_HOST_PORT": str(lokate_port)}
    previous = {key: os.environ.get(key) for key in env}
    os.environ.update(env)
    try:
        yield {"lokate": lokate_port}
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def client(http_url: str, ws_url: str, token: str) -> Lokate:
    """A client that authenticates with one of the static tokens of configs/lokate.yaml."""

    async def token_loader() -> str:
        return token

    return Lokate(
        rath=LokateRath(
            link=compose(
                TimeoutLink(timeout=12),
                ComposedAuthLink(token_loader=token_loader, token_refresher=token_loader),
                SplitLink(
                    left=AIOHttpLink(endpoint_url=http_url),
                    right=GraphQLWSLink(ws_endpoint_url=ws_url),
                    split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                ),
            ),
        ),
    )


@dataclass
class DeployedLokate:
    """Deployed Lokate instance, and a client per static token."""

    deployment: Deployment
    lokate_watcher: LogWatcher
    phone_a: Lokate
    phone_b: Lokate
    other: Lokate


@pytest.fixture(scope="session")
def deployed_app(
    integration_ports: dict[str, int],
) -> Generator[DeployedLokate, None, None]:
    """lokate and its database (postgres + PostGIS), via Docker Compose."""
    # testing(): a per-run `dokker-test-<hash>` project that is torn down on
    # exit, so concurrent or crashed runs (and sibling repos, which all name
    # their stack `integration`) never share containers.
    setup = testing(compose_files)
    setup.add_health_check(
        url=lambda spec: (
            f"http://localhost:{spec.find_service('lokate').get_port_for_internal(80).published}/graphql"
        ),
        service="lokate",
        timeout=5,
        # dokker sleeps `timeout` seconds between attempts: 20 x 5 s covers a
        # cold backend on a two-core runner.
        max_retries=20,
    )

    watcher = setup.create_watcher("lokate")

    with setup:
        setup.down()
        try:
            setup.pull()
        except Exception as error:  # noqa: BLE001 -- best effort, see below
            # Best effort: Docker Hub rate-limits anonymous pulls, and a locally
            # built image (docker-compose.local.yml) has nothing to pull. A
            # genuinely missing image still fails loudly, at `up`.
            print(f"Could not refresh the images, using the local ones: {error}")
        setup.inspect()

        port = setup.spec.find_service("lokate").get_port_for_internal(80).published
        http_url = f"http://localhost:{port}/graphql"
        ws_url = f"ws://localhost:{port}/graphql"

        setup.up()
        setup.check_health()

        phone_a = client(http_url, ws_url, "phone-a")
        phone_b = client(http_url, ws_url, "phone-b")
        other = client(http_url, ws_url, "other")
        with phone_a, phone_b, other:
            yield DeployedLokate(
                deployment=setup,
                lokate_watcher=watcher,
                phone_a=phone_a,
                phone_b=phone_b,
                other=other,
            )


@pytest.fixture(scope="session")
def lokate(deployed_app: DeployedLokate) -> Lokate:
    """The first phone's client: API calls are its methods, nothing is ambient."""
    return deployed_app.phone_a
