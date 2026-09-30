"""The backup protocol through the client, against a real lokate (and postgres + PostGIS).

``phone_a`` and ``phone_b`` are one user's two phones; ``other`` is another user. The
stack is shared by the session, so each test uses its own client ids.
"""

import datetime
import uuid

import pytest

from lokate.api.schema import DeletedInput, PlaceInput, PointInput, TripInput, TripMode, VisitInput
from lokate.lokate import Lokate
from tests.conftest import DeployedLokate

pytestmark = pytest.mark.integration

T0 = datetime.datetime(2026, 8, 30, 12, 0, tzinfo=datetime.timezone.utc)


def at(minutes: float) -> datetime.datetime:
    return T0 + datetime.timedelta(minutes=minutes)


def unique() -> str:
    return uuid.uuid4().hex[:8]


def points(prefix: str, n: int) -> list[PointInput]:
    return [PointInput(client_id=f"{prefix}-{i}", ts=at(i), lat=48.2 + i * 1e-4, lon=16.37, acc=5.0) for i in range(n)]


def all_changes(lokate: Lokate) -> tuple[set[str], set[str], set[str], set[str], set[str]]:
    """Page ``changes`` to the end; every client id seen, per kind. Nothing may arrive twice."""
    seen: list[set] = [set(), set(), set(), set(), set()]
    cursor = None
    while True:
        page = lokate.get_changes(cursor=cursor, limit=50)
        keyed = (
            [(p.device_id, p.client_id) for p in page.points],
            [(v.device_id, v.client_id) for v in page.visits],
            [(t.device_id, t.client_id) for t in page.trips],
            [(None, p.client_id) for p in page.places],
            [(None, c) for c in page.deleted_places],
        )
        for bucket, keys in zip(seen, keyed):
            for key in keys:
                assert key not in bucket, f"{key} delivered twice"
                bucket.add(key)
        cursor = page.next_cursor
        if not page.has_more:
            return tuple({client_id for _, client_id in bucket} for bucket in seen)  # type: ignore[return-value]


def test_a_retried_upload_changes_nothing(lokate: Lokate) -> None:
    batch = points(unique(), 30)
    first = lokate.upload_points(batch)
    assert (first.accepted, first.duplicates) == (30, 0)
    again = lokate.upload_points(batch)
    assert (again.accepted, again.duplicates) == (0, 30)


def test_batches_over_1000_are_refused(lokate: Lokate) -> None:
    with pytest.raises(Exception, match="at most 1000"):
        lokate.upload_points(points(unique(), 1001))


def test_replace_segments_is_per_device(deployed_app: DeployedLokate) -> None:
    tag = unique()
    start = at(60 * 24 * 30)  # a window of its own
    visits = [VisitInput(client_id=f"{tag}-v1", start=start, end=start + datetime.timedelta(minutes=10), lat=48.2, lon=16.37, radius=40.0, point_count=12)]
    trips = [TripInput(client_id=f"{tag}-t1", start=start + datetime.timedelta(minutes=10), end=start + datetime.timedelta(minutes=20), distance=900.0, mode=TripMode.BIKE, from_visit=f"{tag}-v1")]

    deployed_app.phone_a.replace_segments(from_=start, visits=visits, trips=trips)
    deployed_app.phone_b.replace_segments(from_=start, visits=visits, trips=[])

    # Phone A empties its window; phone B's copy of the same client ids is untouched.
    result = deployed_app.phone_a.replace_segments(from_=start, visits=[], trips=[])
    assert (result.deleted_visits, result.deleted_trips) == (1, 1)
    retry = deployed_app.phone_a.replace_segments(from_=start, visits=[], trips=[])
    assert (retry.deleted_visits, retry.deleted_trips) == (0, 0)

    state = deployed_app.phone_b.get_sync_state()
    assert state.segments_from == start
    _, visit_ids, _, _, _ = all_changes(deployed_app.phone_b)
    assert f"{tag}-v1" in visit_ids


def test_places_last_write_wins_and_tombstones(deployed_app: DeployedLokate) -> None:
    home, gym = f"home-{unique()}", f"gym-{unique()}"
    a, b = deployed_app.phone_a, deployed_app.phone_b

    a.merge_places(places=[PlaceInput(client_id=home, name="Home", lat=1.0, lon=2.0, radius=80.0, updated_at=at(10)), PlaceInput(client_id=gym, name="Gym", lat=1.0, lon=2.0, radius=80.0, updated_at=at(10))], deleted=[])
    a.merge_places(places=[], deleted=[DeletedInput(client_id=gym, deleted_at=at(20))])

    # Phone B holds older copies of both: the newer server copy (and the tombstone) come back.
    result = b.merge_places(places=[PlaceInput(client_id=home, name="Old", lat=1.0, lon=2.0, radius=80.0, updated_at=at(5)), PlaceInput(client_id=gym, name="Gym", lat=1.0, lon=2.0, radius=80.0, updated_at=at(15))], deleted=[])
    assert result.applied == 0
    stale = {p.client_id: p for p in result.stale}
    assert stale[home].name == "Home" and stale[home].deleted_at is None
    assert stale[gym].deleted_at == at(20)

    _, _, _, place_ids, deleted_ids = all_changes(b)
    assert home in place_ids and gym in deleted_ids


def test_restore_pulls_every_device_and_no_other_user(deployed_app: DeployedLokate) -> None:
    tag = unique()
    deployed_app.phone_a.upload_points(points(f"{tag}-a", 120))
    deployed_app.phone_b.upload_points(points(f"{tag}-b", 70))
    deployed_app.other.upload_points(points(f"{tag}-x", 10))

    point_ids, *_ = all_changes(deployed_app.phone_b)
    mine = {i for i in point_ids if i.startswith(tag)}
    assert mine == {f"{tag}-a-{i}" for i in range(120)} | {f"{tag}-b-{i}" for i in range(70)}


def test_delete_server_copy(deployed_app: DeployedLokate) -> None:
    other = deployed_app.other
    other.upload_points(points(unique(), 5))
    with pytest.raises(Exception, match="DELETE"):
        other.delete_server_copy("yes")
    assert other.delete_server_copy("DELETE") >= 5
    assert other.get_sync_state().point_count == 0
    # The first user's data is untouched.
    assert deployed_app.phone_a.get_sync_state().point_count > 0
