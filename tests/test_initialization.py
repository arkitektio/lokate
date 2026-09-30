"""Lightweight initialization tests that need no deployed stack.

These run on every OS in the CI matrix (they carry no ``integration`` marker),
exercising pure-Python construction of the client and the generated schema
models without touching the network or Docker.
"""

import datetime
import inspect

from lokate.api.schema import (
    DeletedInput,
    PlaceInput,
    PointInput,
    ReplaceSegmentsMutation,
    TripInput,
    TripMode,
    VisitInput,
)
from lokate.lokate import Lokate

T = datetime.datetime(2026, 9, 1, 12, tzinfo=datetime.timezone.utc)


def test_lokate_importable() -> None:
    """The top-level ``Lokate`` composition imports and is a class."""
    assert isinstance(Lokate, type)


def test_inputs_speak_the_wire_names() -> None:
    """Python names in, GraphQL names out; unset optionals stay off the wire."""
    point = PointInput(client_id="p1", ts=T, lat=48.2, lon=16.37)
    assert point.model_dump(by_alias=True, exclude_unset=True) == {"clientId": "p1", "ts": T, "lat": 48.2, "lon": 16.37}
    visit = VisitInput(client_id="v1", start=T, end=T, lat=1.0, lon=2.0, radius=50.0, point_count=3)
    assert visit.model_dump(by_alias=True, exclude_unset=True)["pointCount"] == 3
    trip = TripInput(client_id="t1", start=T, end=T, distance=10.0, mode=TripMode.WALK, from_visit="v1")
    assert trip.model_dump(by_alias=True, exclude_unset=True)["fromVisit"] == "v1"
    assert PlaceInput(client_id="home", name="Home", lat=1.0, lon=2.0, radius=80.0, updated_at=T).model_dump(by_alias=True)["updatedAt"] == T
    assert DeletedInput(client_id="gym", deleted_at=T).model_dump(by_alias=True) == {"clientId": "gym", "deletedAt": T}


def test_from_is_a_python_name_and_the_wire_name() -> None:
    """``from`` is a keyword: the method takes ``from_``, the wire carries ``from``."""
    parameters = inspect.signature(Lokate.replace_segments).parameters
    assert list(parameters)[1:4] == ["from_", "visits", "trips"]
    arguments = ReplaceSegmentsMutation.Arguments(from_=T, visits=[], trips=[])
    assert arguments.model_dump(by_alias=True)["from"] == T


def test_defaulted_arguments_are_optional_keywords() -> None:
    """What the server defaults, the caller may leave out."""
    for method, required in {
        Lokate.get_changes: set(),
        Lokate.list_points: set(),
        Lokate.get_day: {"date"},
        Lokate.get_route: {"since", "until"},
        Lokate.get_stats: {"since", "until"},
        Lokate.upload_points: {"points"},
        Lokate.merge_places: {"places", "deleted"},
        Lokate.delete_server_copy: {"confirm"},
    }.items():
        parameters = inspect.signature(method).parameters.values()
        assert {p.name for p in parameters if p.default is inspect.Parameter.empty} - {"self"} == required, method


def test_every_method_takes_the_task_kwarg() -> None:
    """``task=`` is the rekuest task a call is attributed to, on every method."""
    for name in ("upload_points", "replace_segments", "merge_places", "get_changes"):
        parameters = inspect.signature(getattr(Lokate, name)).parameters
        assert str(parameters["task"].annotation).endswith("TaskLike | None")
