"""Reading the timeline back through the client, against a real lokate."""

import datetime
import json
import uuid

import pytest

from lokate.api.schema import Granularity, PointFilter, PointInput, TripInput, TripMode, VisitInput
from tests.conftest import DeployedLokate

pytestmark = pytest.mark.integration

UTC = datetime.timezone.utc


def test_reads(deployed_app: DeployedLokate) -> None:
    lokate = deployed_app.phone_b
    tag = uuid.uuid4().hex[:8]
    # A day of its own, far from what the other tests write.
    t0 = datetime.datetime(2026, 3, 1 + int(tag, 16) % 27, 9, 0, tzinfo=UTC)
    fixes = [PointInput(client_id=f"{tag}-{i}", ts=t0 + datetime.timedelta(minutes=i), lat=48.20 + i * 0.001, lon=16.37, acc=5.0) for i in range(10)]
    lokate.upload_points(fixes)
    lokate.replace_segments(
        from_=t0,
        visits=[VisitInput(client_id=f"{tag}-v", start=t0 + datetime.timedelta(minutes=10), end=t0 + datetime.timedelta(hours=2), lat=48.21, lon=16.37, radius=30.0, point_count=4)],
        trips=[TripInput(client_id=f"{tag}-t", start=t0, end=t0 + datetime.timedelta(minutes=10), distance=1000.0, mode=TripMode.WALK, to_visit=f"{tag}-v")],
    )

    window = PointFilter(since=t0, until=t0 + datetime.timedelta(hours=1))
    assert lokate.count_points(filters=window) == 10
    listed = lokate.list_points(filters=window, pagination={"limit": 3}, ordering=[{"ts": "DESC"}])
    assert [p.client_id for p in listed] == [f"{tag}-9", f"{tag}-8", f"{tag}-7"]

    day = lokate.get_day(date=t0.date(), timezone="UTC")
    [visit] = [v for v in day.visits if v.client_id.startswith(tag)]
    assert (visit.client_id, visit.duration) == (f"{tag}-v", 6600.0)
    assert any(t.mode == TripMode.WALK and t.client_id == f"{tag}-t" for t in day.trips)

    [track] = [t for t in lokate.get_route(since=t0, until=t0 + datetime.timedelta(hours=1)) if t.device.device_id == "phone-b"]
    line = json.loads(track.geojson)
    assert line["type"] == "LineString" and len(line["coordinates"]) == 10
    assert track.distance > 900

    buckets = lokate.get_stats(since=t0, until=t0 + datetime.timedelta(days=1), granularity=Granularity.DAY)
    assert buckets[0].point_count >= 10 and buckets[0].trip_count >= 1

    devices = lokate.list_devices()
    assert "phone-b" in {d.device_id for d in devices}
