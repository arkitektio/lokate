import builtins
from datetime import date, datetime
from enum import Enum
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from rath.scalars import ID, IDCoercible
from rath.task import TaskLike
from typing import Annotated, Literal

class GraphQLDefault:
    """Records a GraphQL field schema default value. The client omits the field so the server applies its own default; this preserves the value for introspection."""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'GraphQLDefault(' + repr(self.value) + ')'

class UnsetType:
    """Sentinel for arguments the caller did not provide. Such fields are omitted on serialization so the GraphQL server applies its own default."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'UNSET'

    def __bool__(self):
        return False
UNSET = UnsetType()

class Granularity(str, Enum):
    """The width of a stats bucket."""
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    __str__ = str.__str__

class Ordering(str, Enum):
    """No documentation"""
    ASC = 'ASC'
    ASC_NULLS_FIRST = 'ASC_NULLS_FIRST'
    ASC_NULLS_LAST = 'ASC_NULLS_LAST'
    DESC = 'DESC'
    DESC_NULLS_FIRST = 'DESC_NULLS_FIRST'
    DESC_NULLS_LAST = 'DESC_NULLS_LAST'
    __str__ = str.__str__

class TripMode(str, Enum):
    """How a trip was travelled, as the phone classified it."""
    WALK = 'WALK'
    BIKE = 'BIKE'
    VEHICLE = 'VEHICLE'
    UNKNOWN = 'UNKNOWN'
    __str__ = str.__str__

class BoxInput(BaseModel):
    """A lat/lon rectangle, e.g. a map viewport."""
    south: float
    west: float
    north: float
    east: float
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeletedInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    deleted_at: datetime = Field(validation_alias=AliasChoices('deleted_at', 'deletedAt'), serialization_alias='deletedAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeviceFilter(BaseModel):
    """One phone (install) of a user: the ``client_device`` claim of its token.

Keyed by user as well, so two accounts on one phone never share rows. A reinstall that
is issued a new device id is a new ``Device``; its old one's history stays readable
through ``changes``."""
    and_: 'DeviceFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'DeviceFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'DeviceFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeviceOrderFirstSeenAt(BaseModel):
    """'firstSeenAt' variant of the @oneOf input 'DeviceOrder'"""
    first_seen_at: Ordering = Field(validation_alias=AliasChoices('first_seen_at', 'firstSeenAt'), serialization_alias='firstSeenAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class DeviceOrderLastUploadAt(BaseModel):
    """'lastUploadAt' variant of the @oneOf input 'DeviceOrder'"""
    last_upload_at: Ordering = Field(validation_alias=AliasChoices('last_upload_at', 'lastUploadAt'), serialization_alias='lastUploadAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
DeviceOrder = DeviceOrderFirstSeenAt | DeviceOrderLastUploadAt

class NearInput(BaseModel):
    """Within `radius` meters of a point."""
    lat: float
    lon: float
    radius: float
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class OffsetPaginationInput(BaseModel):
    """No documentation"""
    offset: Annotated[int | None, GraphQLDefault('0')] = None
    'Default: 0'
    limit: int | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PlaceFilter(BaseModel):
    """A named place, shared by all of a user's phones (so keyed by user, not device).

Last write wins on ``updated_at``. A deleted place stays as a tombstone (``deleted_at``
set) so another phone's older copy is not uploaded again. A tombstone can arrive for a
place the server never saw, so everything but the key and the stamps is nullable."""
    and_: 'PlaceFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'PlaceFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'PlaceFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    ids: tuple[ID, ...] | None = None
    search: str | None = None
    in_box: BoxInput | None = Field(validation_alias=AliasChoices('in_box', 'inBox'), serialization_alias='inBox', default=None)
    near: NearInput | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PlaceInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    name: str
    lat: float
    lon: float
    radius: float
    updated_at: datetime = Field(validation_alias=AliasChoices('updated_at', 'updatedAt'), serialization_alias='updatedAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PlaceOrderName(BaseModel):
    """'name' variant of the @oneOf input 'PlaceOrder'"""
    name: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PlaceOrderUpdatedAt(BaseModel):
    """'updatedAt' variant of the @oneOf input 'PlaceOrder'"""
    updated_at: Ordering = Field(validation_alias=AliasChoices('updated_at', 'updatedAt'), serialization_alias='updatedAt')
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
PlaceOrder = PlaceOrderName | PlaceOrderUpdatedAt

class PointFilter(BaseModel):
    """One location fix. Partitioned by month of ``ts`` (see the module docstring)."""
    and_: 'PointFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'PointFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'PointFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    devices: tuple[ID, ...] | None = None
    since: datetime | None = None
    until: datetime | None = None
    in_box: BoxInput | None = Field(validation_alias=AliasChoices('in_box', 'inBox'), serialization_alias='inBox', default=None)
    near: NearInput | None = None
    max_accuracy: float | None = Field(validation_alias=AliasChoices('max_accuracy', 'maxAccuracy'), serialization_alias='maxAccuracy', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PointInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    ts: datetime
    lat: float
    lon: float
    acc: float | None = None
    speed: float | None = None
    heading: float | None = None
    alt: float | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class PointOrderTs(BaseModel):
    """'ts' variant of the @oneOf input 'PointOrder'"""
    ts: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
PointOrder = PointOrderTs

class TripFilter(BaseModel):
    """A movement between two visits, as the phone segmented it."""
    and_: 'TripFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'TripFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'TripFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    devices: tuple[ID, ...] | None = None
    since: datetime | None = None
    until: datetime | None = None
    modes: tuple[TripMode, ...] | None = None
    min_distance: float | None = Field(validation_alias=AliasChoices('min_distance', 'minDistance'), serialization_alias='minDistance', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TripInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    start: datetime
    end: datetime
    distance: float
    mode: TripMode
    from_visit: ID | None = Field(validation_alias=AliasChoices('from_visit', 'fromVisit'), serialization_alias='fromVisit', default=None)
    to_visit: ID | None = Field(validation_alias=AliasChoices('to_visit', 'toVisit'), serialization_alias='toVisit', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TripOrderStart(BaseModel):
    """'start' variant of the @oneOf input 'TripOrder'"""
    start: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class TripOrderDistance(BaseModel):
    """'distance' variant of the @oneOf input 'TripOrder'"""
    distance: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
TripOrder = TripOrderStart | TripOrderDistance

class VisitFilter(BaseModel):
    """A stay at one spot, as the phone segmented it."""
    and_: 'VisitFilter | None' = Field(validation_alias=AliasChoices('and_', 'AND'), serialization_alias='AND', default=None)
    or_: 'VisitFilter | None' = Field(validation_alias=AliasChoices('or_', 'OR'), serialization_alias='OR', default=None)
    not_: 'VisitFilter | None' = Field(validation_alias=AliasChoices('not_', 'NOT'), serialization_alias='NOT', default=None)
    distinct: bool | None = Field(validation_alias=AliasChoices('distinct', 'DISTINCT'), serialization_alias='DISTINCT', default=None)
    devices: tuple[ID, ...] | None = None
    since: datetime | None = None
    until: datetime | None = None
    places: tuple[ID, ...] | None = None
    has_place: bool | None = Field(validation_alias=AliasChoices('has_place', 'hasPlace'), serialization_alias='hasPlace', default=None)
    min_duration: float | None = Field(validation_alias=AliasChoices('min_duration', 'minDuration'), serialization_alias='minDuration', default=None)
    in_box: BoxInput | None = Field(validation_alias=AliasChoices('in_box', 'inBox'), serialization_alias='inBox', default=None)
    near: NearInput | None = None
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class VisitInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    start: datetime
    end: datetime
    lat: float
    lon: float
    radius: float
    point_count: int = Field(validation_alias=AliasChoices('point_count', 'pointCount'), serialization_alias='pointCount')
    place_client_id: ID | None = Field(validation_alias=AliasChoices('place_client_id', 'placeClientId'), serialization_alias='placeClientId', default=None)
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class VisitOrderStart(BaseModel):
    """'start' variant of the @oneOf input 'VisitOrder'"""
    start: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)

class VisitOrderEnd(BaseModel):
    """'end' variant of the @oneOf input 'VisitOrder'"""
    end: Ordering
    model_config = ConfigDict(frozen=True, extra='forbid', populate_by_name=True, use_enum_values=True)
VisitOrder = VisitOrderStart | VisitOrderEnd

class ModeStat(BaseModel):
    """Trips of one mode within a stats bucket."""
    typename: Literal['ModeStat'] = Field(alias='__typename', default='ModeStat', exclude=True)
    mode: TripMode
    trips: int
    distance: float
    'Meters.'
    seconds: float
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ModeStat"""
        document = 'fragment ModeStat on ModeStat {\n  mode\n  trips\n  distance\n  seconds\n  __typename\n}'
        name = 'ModeStat'
        type = 'ModeStat'

class SyncState(BaseModel):
    """The calling device's watermarks."""
    typename: Literal['SyncState'] = Field(alias='__typename', default='SyncState', exclude=True)
    last_point_ts: datetime | None = Field(default=None, alias='lastPointTs')
    point_count: int = Field(alias='pointCount')
    segments_from: datetime | None = Field(default=None, alias='segmentsFrom')
    "The `from` of this device's last replaceSegments."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for SyncState"""
        document = 'fragment SyncState on SyncState {\n  lastPointTs\n  pointCount\n  segmentsFrom\n  __typename\n}'
        name = 'SyncState'
        type = 'SyncState'

class UploadResult(BaseModel):
    """No documentation"""
    typename: Literal['UploadResult'] = Field(alias='__typename', default='UploadResult', exclude=True)
    accepted: int
    duplicates: int
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for UploadResult"""
        document = 'fragment UploadResult on UploadResult {\n  accepted\n  duplicates\n  __typename\n}'
        name = 'UploadResult'
        type = 'UploadResult'

class ReplaceResult(BaseModel):
    """No documentation"""
    typename: Literal['ReplaceResult'] = Field(alias='__typename', default='ReplaceResult', exclude=True)
    deleted_visits: int = Field(alias='deletedVisits')
    deleted_trips: int = Field(alias='deletedTrips')
    visits: int
    trips: int
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ReplaceResult"""
        document = 'fragment ReplaceResult on ReplaceResult {\n  deletedVisits\n  deletedTrips\n  visits\n  trips\n  __typename\n}'
        name = 'ReplaceResult'
        type = 'ReplaceResult'

class Device(BaseModel):
    """One of your phones (an install): the token's client_device."""
    typename: Literal['Device'] = Field(alias='__typename', default='Device', exclude=True)
    id: ID
    device_id: str = Field(alias='deviceId')
    'The client_device claim it uploads with.'
    first_seen_at: datetime = Field(alias='firstSeenAt')
    last_upload_at: datetime | None = Field(default=None, alias='lastUploadAt')
    'When this device last wrote anything.'
    segments_from: datetime | None = Field(default=None, alias='segmentsFrom')
    'The `from` of its last replaceSegments.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Device"""
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}'
        name = 'Device'
        type = 'Device'

class Point(BaseModel):
    """One location fix."""
    typename: Literal['Point'] = Field(alias='__typename', default='Point', exclude=True)
    id: ID
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    'The client_device of the device that recorded it.'
    ts: datetime
    lat: float
    lon: float
    acc: float | None = Field(default=None)
    'Horizontal accuracy, meters.'
    speed: float | None = Field(default=None)
    'Meters per second.'
    heading: float | None = Field(default=None)
    'Degrees from north.'
    alt: float | None = Field(default=None)
    'Altitude, meters.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Point"""
        document = 'fragment Point on Point {\n  id\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}'
        name = 'Point'
        type = 'Point'

class Place(BaseModel):
    """A named place, shared by all of your phones."""
    typename: Literal['Place'] = Field(alias='__typename', default='Place', exclude=True)
    id: ID
    client_id: ID = Field(alias='clientId')
    name: str | None = Field(default=None)
    lat: float | None = Field(default=None)
    lon: float | None = Field(default=None)
    radius: float | None = Field(default=None)
    'Meters.'
    updated_at: datetime = Field(alias='updatedAt')
    "The phone's edit time; last write wins on it."
    deleted_at: datetime | None = Field(default=None, alias='deletedAt')
    "Set on a tombstone (only ever seen in syncPlaces' `stale`)."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Place"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}'
        name = 'Place'
        type = 'Place'

class Visit(BaseModel):
    """A stay at one spot."""
    typename: Literal['Visit'] = Field(alias='__typename', default='Visit', exclude=True)
    id: ID
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    'The client_device of the device that recorded it.'
    start: datetime
    end: datetime
    lat: float
    lon: float
    radius: float
    'Meters.'
    point_count: int = Field(alias='pointCount')
    place_client_id: ID | None = Field(default=None, alias='placeClientId')
    'The clientId of the place it was matched to.'
    duration: float
    'How long it lasted, seconds.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Visit"""
        document = 'fragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}'
        name = 'Visit'
        type = 'Visit'

class Trip(BaseModel):
    """A movement between two visits."""
    typename: Literal['Trip'] = Field(alias='__typename', default='Trip', exclude=True)
    id: ID
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    'The client_device of the device that recorded it.'
    start: datetime
    end: datetime
    from_visit: ID | None = Field(default=None, alias='fromVisit')
    'The clientId of the visit it left.'
    to_visit: ID | None = Field(default=None, alias='toVisit')
    'The clientId of the visit it arrived at.'
    distance: float
    'Meters.'
    mode: TripMode
    'How it was travelled.'
    duration: float
    'How long it took, seconds.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Trip"""
        document = 'fragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}'
        name = 'Trip'
        type = 'Trip'

class StatsBucket(BaseModel):
    """Totals for one day, week or month."""
    typename: Literal['StatsBucket'] = Field(alias='__typename', default='StatsBucket', exclude=True)
    start: datetime
    point_count: int = Field(alias='pointCount')
    visit_count: int = Field(alias='visitCount')
    trip_count: int = Field(alias='tripCount')
    distance: float
    'Meters, over all trips.'
    by_mode: tuple[ModeStat, ...] = Field(alias='byMode')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for StatsBucket"""
        document = 'fragment ModeStat on ModeStat {\n  mode\n  trips\n  distance\n  seconds\n  __typename\n}\n\nfragment StatsBucket on StatsBucket {\n  start\n  pointCount\n  visitCount\n  tripCount\n  distance\n  byMode {\n    ...ModeStat\n    __typename\n  }\n  __typename\n}'
        name = 'StatsBucket'
        type = 'StatsBucket'

class Track(BaseModel):
    """One device's points over a time range, joined into a line."""
    typename: Literal['Track'] = Field(alias='__typename', default='Track', exclude=True)
    device: Device
    start: datetime
    end: datetime
    point_count: int = Field(alias='pointCount')
    distance: float
    'Geodesic length of the (unsimplified) line, meters.'
    geojson: str
    'A GeoJSON LineString (coordinates are [lon, lat]).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Track"""
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}\n\nfragment Track on Track {\n  device {\n    ...Device\n    __typename\n  }\n  start\n  end\n  pointCount\n  distance\n  geojson\n  __typename\n}'
        name = 'Track'
        type = 'Track'

class DetailDevice(Device, BaseModel):
    """One of your phones (an install): the token's client_device."""
    typename: Literal['Device'] = Field(alias='__typename', default='Device', exclude=True)
    point_count: int = Field(alias='pointCount')
    'How many points it has uploaded.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailDevice"""
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}\n\nfragment DetailDevice on Device {\n  ...Device\n  pointCount\n  __typename\n}'
        name = 'DetailDevice'
        type = 'Device'

class PlaceStat(BaseModel):
    """Time spent at one place."""
    typename: Literal['PlaceStat'] = Field(alias='__typename', default='PlaceStat', exclude=True)
    place_client_id: ID = Field(alias='placeClientId')
    place: Place | None = Field(default=None)
    'None if the place was deleted.'
    visit_count: int = Field(alias='visitCount')
    seconds: float
    first_visit_at: datetime = Field(alias='firstVisitAt')
    last_visit_at: datetime = Field(alias='lastVisitAt')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PlaceStat"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceStat on PlaceStat {\n  placeClientId\n  place {\n    ...Place\n    __typename\n  }\n  visitCount\n  seconds\n  firstVisitAt\n  lastVisitAt\n  __typename\n}'
        name = 'PlaceStat'
        type = 'PlaceStat'

class DetailPlace(Place, BaseModel):
    """A named place, shared by all of your phones."""
    typename: Literal['Place'] = Field(alias='__typename', default='Place', exclude=True)
    visit_count: int = Field(alias='visitCount')
    'How many visits were matched to it.'
    last_visit_at: datetime | None = Field(default=None, alias='lastVisitAt')
    'When the latest visit to it ended.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailPlace"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment DetailPlace on Place {\n  ...Place\n  visitCount\n  lastVisitAt\n  __typename\n}'
        name = 'DetailPlace'
        type = 'Place'

class PlaceSyncResult(BaseModel):
    """No documentation"""
    typename: Literal['PlaceSyncResult'] = Field(alias='__typename', default='PlaceSyncResult', exclude=True)
    applied: int
    stale: tuple[Place, ...]
    'Places whose server copy is newer; the phone takes them (deletedAt set: delete it).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for PlaceSyncResult"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceSyncResult on PlaceSyncResult {\n  applied\n  stale {\n    ...Place\n    __typename\n  }\n  __typename\n}'
        name = 'PlaceSyncResult'
        type = 'PlaceSyncResult'

class DetailVisit(Visit, BaseModel):
    """A stay at one spot."""
    typename: Literal['Visit'] = Field(alias='__typename', default='Visit', exclude=True)
    place: Place | None = Field(default=None)
    'The place it was matched to (none if deleted or unmatched).'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for DetailVisit"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment DetailVisit on Visit {\n  ...Visit\n  place {\n    ...Place\n    __typename\n  }\n  __typename\n}'
        name = 'DetailVisit'
        type = 'Visit'

class ChangeSet(BaseModel):
    """One page of everything the user has, from all their devices, in change order."""
    typename: Literal['ChangeSet'] = Field(alias='__typename', default='ChangeSet', exclude=True)
    points: tuple[Point, ...]
    visits: tuple[Visit, ...]
    trips: tuple[Trip, ...]
    places: tuple[Place, ...]
    deleted_places: tuple[ID, ...] = Field(alias='deletedPlaces')
    next_cursor: str | None = Field(default=None, alias='nextCursor')
    has_more: bool = Field(alias='hasMore')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for ChangeSet"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Point on Point {\n  id\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nfragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment ChangeSet on ChangeSet {\n  points {\n    ...Point\n    __typename\n  }\n  visits {\n    ...Visit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  places {\n    ...Place\n    __typename\n  }\n  deletedPlaces\n  nextCursor\n  hasMore\n  __typename\n}'
        name = 'ChangeSet'
        type = 'ChangeSet'

class Day(BaseModel):
    """One calendar day of the timeline, across all your devices."""
    typename: Literal['Day'] = Field(alias='__typename', default='Day', exclude=True)
    date: date
    start: datetime
    'Midnight, in the requested time zone.'
    end: datetime
    visits: tuple[DetailVisit, ...]
    'Visits overlapping the day, oldest first.'
    trips: tuple[Trip, ...]
    'Trips overlapping the day, oldest first.'
    point_count: int = Field(alias='pointCount')
    distance: float
    "Meters travelled, summed over the day's trips."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Day"""
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment DetailVisit on Visit {\n  ...Visit\n  place {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nfragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nfragment Day on Day {\n  date\n  start\n  end\n  visits {\n    ...DetailVisit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  pointCount\n  distance\n  __typename\n}'
        name = 'Day'
        type = 'Day'

class DeleteServerCopyMutation(BaseModel):
    """ Delete all of your data on the server; `confirm` must be "DELETE". Returns how many rows went."""
    delete_server_copy: int = Field(alias='deleteServerCopy')
    'Delete all of your data on this server (confirm = "DELETE"). Returns how many points, visits, trips and places were deleted.'

    class Arguments(BaseModel):
        """Arguments for DeleteServerCopy """
        confirm: str

    class Meta:
        """Meta class for DeleteServerCopy """
        document = 'mutation DeleteServerCopy($confirm: String!) {\n  deleteServerCopy(confirm: $confirm)\n}'

class UploadPointsMutation(BaseModel):
    """ Store points (at most 1000 per call). Safe to repeat: a point already stored counts as a duplicate."""
    upload_points: UploadResult = Field(alias='uploadPoints')
    'Store points (at most 1000 per call). Safe to repeat: a point already stored counts as a duplicate.'

    class Arguments(BaseModel):
        """Arguments for UploadPoints """
        points: list[PointInput]

    class Meta:
        """Meta class for UploadPoints """
        document = 'fragment UploadResult on UploadResult {\n  accepted\n  duplicates\n  __typename\n}\n\nmutation UploadPoints($points: [PointInput!]!) {\n  uploadPoints(points: $points) {\n    ...UploadResult\n    __typename\n  }\n}'

class ReplaceSegmentsMutation(BaseModel):
    """ In one transaction, make this device's visits and trips starting at or after `from` exactly the ones sent."""
    replace_segments: ReplaceResult = Field(alias='replaceSegments')
    "In one transaction, make this device's visits and trips starting at or after `from` exactly the ones sent."

    class Arguments(BaseModel):
        """Arguments for ReplaceSegments """
        from_: datetime = Field(validation_alias=AliasChoices('from_', 'from'), serialization_alias='from')
        visits: list[VisitInput]
        trips: list[TripInput]

    class Meta:
        """Meta class for ReplaceSegments """
        document = 'fragment ReplaceResult on ReplaceResult {\n  deletedVisits\n  deletedTrips\n  visits\n  trips\n  __typename\n}\n\nmutation ReplaceSegments($from: DateTime!, $visits: [VisitInput!]!, $trips: [TripInput!]!) {\n  replaceSegments(from: $from, visits: $visits, trips: $trips) {\n    ...ReplaceResult\n    __typename\n  }\n}'

class MergePlacesMutation(BaseModel):
    """ Merge places and tombstones, last write wins on updatedAt; newer server copies come back in `stale`."""
    sync_places: PlaceSyncResult = Field(alias='syncPlaces')
    'Merge places and tombstones, last write wins on updatedAt; newer server copies come back in `stale`.'

    class Arguments(BaseModel):
        """Arguments for MergePlaces """
        places: list[PlaceInput]
        deleted: list[DeletedInput]

    class Meta:
        """Meta class for MergePlaces """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceSyncResult on PlaceSyncResult {\n  applied\n  stale {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nmutation MergePlaces($places: [PlaceInput!]!, $deleted: [DeletedInput!]!) {\n  syncPlaces(places: $places, deleted: $deleted) {\n    ...PlaceSyncResult\n    __typename\n  }\n}'

class GetDayQuery(BaseModel):
    """ One calendar day (in `timezone`, an IANA name): its visits and trips in order, and totals."""
    day: Day
    'One calendar day (in `timezone`, IANA name): its visits and trips in order, and totals.'

    class Arguments(BaseModel):
        """Arguments for GetDay """
        date: date
        timezone: str | None = Field(default=None)

    class Meta:
        """Meta class for GetDay """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment DetailVisit on Visit {\n  ...Visit\n  place {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nfragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nfragment Day on Day {\n  date\n  start\n  end\n  visits {\n    ...DetailVisit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  pointCount\n  distance\n  __typename\n}\n\nquery GetDay($date: Date!, $timezone: String) {\n  day(date: $date, timezone: $timezone) {\n    ...Day\n    __typename\n  }\n}'

class GetRouteQuery(BaseModel):
    """ Your path between `since` and `until`: one GeoJSON LineString per device."""
    route: tuple[Track, ...]
    'Your path between `since` and `until`, one GeoJSON line per device.'

    class Arguments(BaseModel):
        """Arguments for GetRoute """
        since: datetime
        until: datetime
        devices: list[ID] | None = Field(default=None)
        simplify: float | None = Field(default=None)
        max_accuracy: float | None = Field(validation_alias=AliasChoices('max_accuracy', 'maxAccuracy'), serialization_alias='maxAccuracy', default=None)

    class Meta:
        """Meta class for GetRoute """
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}\n\nfragment Track on Track {\n  device {\n    ...Device\n    __typename\n  }\n  start\n  end\n  pointCount\n  distance\n  geojson\n  __typename\n}\n\nquery GetRoute($since: DateTime!, $until: DateTime!, $devices: [ID!], $simplify: Float, $maxAccuracy: Float) {\n  route(\n    since: $since\n    until: $until\n    devices: $devices\n    simplify: $simplify\n    maxAccuracy: $maxAccuracy\n  ) {\n    ...Track\n    __typename\n  }\n}'

class GetStatsQuery(BaseModel):
    """ Points, visits, trips and distance per day, week or month."""
    stats: tuple[StatsBucket, ...]
    'Points, visits, trips and distance per day, week or month.'

    class Arguments(BaseModel):
        """Arguments for GetStats """
        since: datetime
        until: datetime
        granularity: Granularity | None = Field(default=None)
        timezone: str | None = Field(default=None)

    class Meta:
        """Meta class for GetStats """
        document = 'fragment ModeStat on ModeStat {\n  mode\n  trips\n  distance\n  seconds\n  __typename\n}\n\nfragment StatsBucket on StatsBucket {\n  start\n  pointCount\n  visitCount\n  tripCount\n  distance\n  byMode {\n    ...ModeStat\n    __typename\n  }\n  __typename\n}\n\nquery GetStats($since: DateTime!, $until: DateTime!, $granularity: Granularity, $timezone: String) {\n  stats(\n    since: $since\n    until: $until\n    granularity: $granularity\n    timezone: $timezone\n  ) {\n    ...StatsBucket\n    __typename\n  }\n}'

class GetPlaceStatsQuery(BaseModel):
    """ Time spent per place, most first."""
    place_stats: tuple[PlaceStat, ...] = Field(alias='placeStats')
    'Time spent per place, most first.'

    class Arguments(BaseModel):
        """Arguments for GetPlaceStats """
        since: datetime | None = Field(default=None)
        until: datetime | None = Field(default=None)
        limit: int | None = Field(default=None)

    class Meta:
        """Meta class for GetPlaceStats """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceStat on PlaceStat {\n  placeClientId\n  place {\n    ...Place\n    __typename\n  }\n  visitCount\n  seconds\n  firstVisitAt\n  lastVisitAt\n  __typename\n}\n\nquery GetPlaceStats($since: DateTime, $until: DateTime, $limit: Int) {\n  placeStats(since: $since, until: $until, limit: $limit) {\n    ...PlaceStat\n    __typename\n  }\n}'

class GetSyncStateQuery(BaseModel):
    """ The calling device's watermarks: its newest point, how many, and its last segment window."""
    sync_state: SyncState = Field(alias='syncState')
    "The calling device's watermarks."

    class Arguments(BaseModel):
        """Arguments for GetSyncState """
        pass

    class Meta:
        """Meta class for GetSyncState """
        document = 'fragment SyncState on SyncState {\n  lastPointTs\n  pointCount\n  segmentsFrom\n  __typename\n}\n\nquery GetSyncState {\n  syncState {\n    ...SyncState\n    __typename\n  }\n}'

class GetChangesQuery(BaseModel):
    """ One page of everything you have, from all your devices, changed after `cursor`. Page until hasMore is false."""
    changes: ChangeSet
    'Everything of yours, from all your devices, changed after `cursor`, oldest first (limit at most 1000). Page until hasMore is false; used to restore.'

    class Arguments(BaseModel):
        """Arguments for GetChanges """
        cursor: str | None = Field(default=None)
        limit: int | None = Field(default=None)

    class Meta:
        """Meta class for GetChanges """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Point on Point {\n  id\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nfragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment ChangeSet on ChangeSet {\n  points {\n    ...Point\n    __typename\n  }\n  visits {\n    ...Visit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  places {\n    ...Place\n    __typename\n  }\n  deletedPlaces\n  nextCursor\n  hasMore\n  __typename\n}\n\nquery GetChanges($cursor: String, $limit: Int) {\n  changes(cursor: $cursor, limit: $limit) {\n    ...ChangeSet\n    __typename\n  }\n}'

class ListDevicesQuery(BaseModel):
    """ Your phones (installs) that have backed up here."""
    devices: tuple[DetailDevice, ...]
    'Your phones (installs) that have backed up here.'

    class Arguments(BaseModel):
        """Arguments for ListDevices """
        filters: DeviceFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)
        ordering: list[DeviceOrder] | None = Field(default=None)

    class Meta:
        """Meta class for ListDevices """
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}\n\nfragment DetailDevice on Device {\n  ...Device\n  pointCount\n  __typename\n}\n\nquery ListDevices($filters: DeviceFilter, $pagination: OffsetPaginationInput, $ordering: [DeviceOrder!]) {\n  devices(filters: $filters, pagination: $pagination, ordering: $ordering) {\n    ...DetailDevice\n    __typename\n  }\n}'

class GetDeviceQuery(BaseModel):
    """ A device by id."""
    device: DetailDevice
    'A device by id.'

    class Arguments(BaseModel):
        """Arguments for GetDevice """
        id: ID

    class Meta:
        """Meta class for GetDevice """
        document = 'fragment Device on Device {\n  id\n  deviceId\n  firstSeenAt\n  lastUploadAt\n  segmentsFrom\n  __typename\n}\n\nfragment DetailDevice on Device {\n  ...Device\n  pointCount\n  __typename\n}\n\nquery GetDevice($id: ID!) {\n  device(id: $id) {\n    ...DetailDevice\n    __typename\n  }\n}'

class ListPointsQuery(BaseModel):
    """ Location fixes, filterable by time, device, map box or radius."""
    points: tuple[Point, ...]
    'Location fixes (paginated, filterable by time, device, box or distance).'

    class Arguments(BaseModel):
        """Arguments for ListPoints """
        filters: PointFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)
        ordering: list[PointOrder] | None = Field(default=None)

    class Meta:
        """Meta class for ListPoints """
        document = 'fragment Point on Point {\n  id\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nquery ListPoints($filters: PointFilter, $pagination: OffsetPaginationInput, $ordering: [PointOrder!]) {\n  points(filters: $filters, pagination: $pagination, ordering: $ordering) {\n    ...Point\n    __typename\n  }\n}'

class CountPointsQuery(BaseModel):
    """ How many points match."""
    points_count: int = Field(alias='pointsCount')
    'How many points match (the same filters as `points`).'

    class Arguments(BaseModel):
        """Arguments for CountPoints """
        filters: PointFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountPoints """
        document = 'query CountPoints($filters: PointFilter) {\n  pointsCount(filters: $filters)\n}'

class GetPointQuery(BaseModel):
    """ A point by id."""
    point: Point
    'A point by id.'

    class Arguments(BaseModel):
        """Arguments for GetPoint """
        id: ID

    class Meta:
        """Meta class for GetPoint """
        document = 'fragment Point on Point {\n  id\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nquery GetPoint($id: ID!) {\n  point(id: $id) {\n    ...Point\n    __typename\n  }\n}'

class ListVisitsQuery(BaseModel):
    """ Stays, filterable by time, device, place, duration, map box or radius."""
    visits: tuple[DetailVisit, ...]
    'Stays (paginated, filterable by time, device, place, box or distance).'

    class Arguments(BaseModel):
        """Arguments for ListVisits """
        filters: VisitFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)
        ordering: list[VisitOrder] | None = Field(default=None)

    class Meta:
        """Meta class for ListVisits """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment DetailVisit on Visit {\n  ...Visit\n  place {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nquery ListVisits($filters: VisitFilter, $pagination: OffsetPaginationInput, $ordering: [VisitOrder!]) {\n  visits(filters: $filters, pagination: $pagination, ordering: $ordering) {\n    ...DetailVisit\n    __typename\n  }\n}'

class CountVisitsQuery(BaseModel):
    """ How many visits match."""
    visits_count: int = Field(alias='visitsCount')
    'How many visits match (the same filters as `visits`).'

    class Arguments(BaseModel):
        """Arguments for CountVisits """
        filters: VisitFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountVisits """
        document = 'query CountVisits($filters: VisitFilter) {\n  visitsCount(filters: $filters)\n}'

class GetVisitQuery(BaseModel):
    """ A visit by id."""
    visit: DetailVisit
    'A visit by id.'

    class Arguments(BaseModel):
        """Arguments for GetVisit """
        id: ID

    class Meta:
        """Meta class for GetVisit """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Visit on Visit {\n  id\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  duration\n  __typename\n}\n\nfragment DetailVisit on Visit {\n  ...Visit\n  place {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nquery GetVisit($id: ID!) {\n  visit(id: $id) {\n    ...DetailVisit\n    __typename\n  }\n}'

class ListTripsQuery(BaseModel):
    """ Movements between visits, filterable by time, device, mode or distance."""
    trips: tuple[Trip, ...]
    'Movements between visits (paginated, filterable by time, device, mode or distance).'

    class Arguments(BaseModel):
        """Arguments for ListTrips """
        filters: TripFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)
        ordering: list[TripOrder] | None = Field(default=None)

    class Meta:
        """Meta class for ListTrips """
        document = 'fragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nquery ListTrips($filters: TripFilter, $pagination: OffsetPaginationInput, $ordering: [TripOrder!]) {\n  trips(filters: $filters, pagination: $pagination, ordering: $ordering) {\n    ...Trip\n    __typename\n  }\n}'

class CountTripsQuery(BaseModel):
    """ How many trips match."""
    trips_count: int = Field(alias='tripsCount')
    'How many trips match (the same filters as `trips`).'

    class Arguments(BaseModel):
        """Arguments for CountTrips """
        filters: TripFilter | None = Field(default=None)

    class Meta:
        """Meta class for CountTrips """
        document = 'query CountTrips($filters: TripFilter) {\n  tripsCount(filters: $filters)\n}'

class GetTripQuery(BaseModel):
    """ A trip by id."""
    trip: Trip
    'A trip by id.'

    class Arguments(BaseModel):
        """Arguments for GetTrip """
        id: ID

    class Meta:
        """Meta class for GetTrip """
        document = 'fragment Trip on Trip {\n  id\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  duration\n  __typename\n}\n\nquery GetTrip($id: ID!) {\n  trip(id: $id) {\n    ...Trip\n    __typename\n  }\n}'

class ListPlacesQuery(BaseModel):
    """ Your named places, filterable by name, map box or radius."""
    places: tuple[DetailPlace, ...]
    'Your named places (paginated, filterable by name, box or distance).'

    class Arguments(BaseModel):
        """Arguments for ListPlaces """
        filters: PlaceFilter | None = Field(default=None)
        pagination: OffsetPaginationInput | None = Field(default=None)
        ordering: list[PlaceOrder] | None = Field(default=None)

    class Meta:
        """Meta class for ListPlaces """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment DetailPlace on Place {\n  ...Place\n  visitCount\n  lastVisitAt\n  __typename\n}\n\nquery ListPlaces($filters: PlaceFilter, $pagination: OffsetPaginationInput, $ordering: [PlaceOrder!]) {\n  places(filters: $filters, pagination: $pagination, ordering: $ordering) {\n    ...DetailPlace\n    __typename\n  }\n}'

class GetPlaceQuery(BaseModel):
    """ A place by id."""
    place: DetailPlace
    'A place by id.'

    class Arguments(BaseModel):
        """Arguments for GetPlace """
        id: ID

    class Meta:
        """Meta class for GetPlace """
        document = 'fragment Place on Place {\n  id\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment DetailPlace on Place {\n  ...Place\n  visitCount\n  lastVisitAt\n  __typename\n}\n\nquery GetPlace($id: ID!) {\n  place(id: $id) {\n    ...DetailPlace\n    __typename\n  }\n}'

class LokateApi:
    """Every operation of this API as a method. Generated by turms.

Each method hands its operation to ``execute``, ``aexecute``, ``subscribe``, ``asubscribe`` of ``self``, which the class this one is mixed into (or a base of it) provides."""

    async def adelete_server_copy(self, confirm: str, task: TaskLike | None=None) -> int:
        """DeleteServerCopy 
 Delete all of your data on the server; `confirm` must be "DELETE". Returns how many rows went.

Args:
    confirm (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        variables['confirm'] = confirm
        return (await self.aexecute(DeleteServerCopyMutation, variables, task=task)).delete_server_copy

    def delete_server_copy(self, confirm: str, task: TaskLike | None=None) -> int:
        """DeleteServerCopy 
 Delete all of your data on the server; `confirm` must be "DELETE". Returns how many rows went.

Args:
    confirm (str): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        variables['confirm'] = confirm
        return self.execute(DeleteServerCopyMutation, variables, task=task).delete_server_copy

    async def aupload_points(self, points: list[PointInput], task: TaskLike | None=None) -> UploadResult:
        """UploadPoints 
 Store points (at most 1000 per call). Safe to repeat: a point already stored counts as a duplicate.

Args:
    points (list[PointInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    UploadResult
"""
        variables: dict[str, builtins.object] = {}
        variables['points'] = points
        return (await self.aexecute(UploadPointsMutation, variables, task=task)).upload_points

    def upload_points(self, points: list[PointInput], task: TaskLike | None=None) -> UploadResult:
        """UploadPoints 
 Store points (at most 1000 per call). Safe to repeat: a point already stored counts as a duplicate.

Args:
    points (list[PointInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    UploadResult
"""
        variables: dict[str, builtins.object] = {}
        variables['points'] = points
        return self.execute(UploadPointsMutation, variables, task=task).upload_points

    async def areplace_segments(self, from_: datetime, visits: list[VisitInput], trips: list[TripInput], task: TaskLike | None=None) -> ReplaceResult:
        """ReplaceSegments 
 In one transaction, make this device's visits and trips starting at or after `from` exactly the ones sent.

Args:
    from_ (datetime): No description
    visits (list[VisitInput]): No description
    trips (list[TripInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ReplaceResult
"""
        variables: dict[str, builtins.object] = {}
        variables['from'] = from_
        variables['visits'] = visits
        variables['trips'] = trips
        return (await self.aexecute(ReplaceSegmentsMutation, variables, task=task)).replace_segments

    def replace_segments(self, from_: datetime, visits: list[VisitInput], trips: list[TripInput], task: TaskLike | None=None) -> ReplaceResult:
        """ReplaceSegments 
 In one transaction, make this device's visits and trips starting at or after `from` exactly the ones sent.

Args:
    from_ (datetime): No description
    visits (list[VisitInput]): No description
    trips (list[TripInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ReplaceResult
"""
        variables: dict[str, builtins.object] = {}
        variables['from'] = from_
        variables['visits'] = visits
        variables['trips'] = trips
        return self.execute(ReplaceSegmentsMutation, variables, task=task).replace_segments

    async def amerge_places(self, places: list[PlaceInput], deleted: list[DeletedInput], task: TaskLike | None=None) -> PlaceSyncResult:
        """MergePlaces 
 Merge places and tombstones, last write wins on updatedAt; newer server copies come back in `stale`.

Args:
    places (list[PlaceInput]): No description
    deleted (list[DeletedInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    PlaceSyncResult
"""
        variables: dict[str, builtins.object] = {}
        variables['places'] = places
        variables['deleted'] = deleted
        return (await self.aexecute(MergePlacesMutation, variables, task=task)).sync_places

    def merge_places(self, places: list[PlaceInput], deleted: list[DeletedInput], task: TaskLike | None=None) -> PlaceSyncResult:
        """MergePlaces 
 Merge places and tombstones, last write wins on updatedAt; newer server copies come back in `stale`.

Args:
    places (list[PlaceInput]): No description
    deleted (list[DeletedInput]): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    PlaceSyncResult
"""
        variables: dict[str, builtins.object] = {}
        variables['places'] = places
        variables['deleted'] = deleted
        return self.execute(MergePlacesMutation, variables, task=task).sync_places

    async def aget_day(self, date: date, timezone: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> Day:
        """GetDay 
 One calendar day (in `timezone`, an IANA name): its visits and trips in order, and totals.

Args:
    date (date): No description
    timezone (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Day
"""
        variables: dict[str, builtins.object] = {}
        variables['date'] = date
        if timezone is not UNSET:
            variables['timezone'] = timezone
        return (await self.aexecute(GetDayQuery, variables, task=task)).day

    def get_day(self, date: date, timezone: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> Day:
        """GetDay 
 One calendar day (in `timezone`, an IANA name): its visits and trips in order, and totals.

Args:
    date (date): No description
    timezone (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Day
"""
        variables: dict[str, builtins.object] = {}
        variables['date'] = date
        if timezone is not UNSET:
            variables['timezone'] = timezone
        return self.execute(GetDayQuery, variables, task=task).day

    async def aget_route(self, since: datetime, until: datetime, devices: list[IDCoercible] | None | UnsetType=UNSET, simplify: float | None | UnsetType=UNSET, max_accuracy: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Track, ...]:
        """GetRoute 
 Your path between `since` and `until`: one GeoJSON LineString per device.

Args:
    since (datetime): No description
    until (datetime): No description
    devices (list[ID] | None, optional): No description. 
    simplify (float | None, optional): Tolerance in meters for thinning the line (none: every point).. 
    max_accuracy (float | None, optional): Leave out fixes less accurate than this (meters).. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Track]
"""
        variables: dict[str, builtins.object] = {}
        variables['since'] = since
        variables['until'] = until
        if devices is not UNSET:
            variables['devices'] = devices
        if simplify is not UNSET:
            variables['simplify'] = simplify
        if max_accuracy is not UNSET:
            variables['maxAccuracy'] = max_accuracy
        return (await self.aexecute(GetRouteQuery, variables, task=task)).route

    def get_route(self, since: datetime, until: datetime, devices: list[IDCoercible] | None | UnsetType=UNSET, simplify: float | None | UnsetType=UNSET, max_accuracy: float | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Track, ...]:
        """GetRoute 
 Your path between `since` and `until`: one GeoJSON LineString per device.

Args:
    since (datetime): No description
    until (datetime): No description
    devices (list[ID] | None, optional): No description. 
    simplify (float | None, optional): Tolerance in meters for thinning the line (none: every point).. 
    max_accuracy (float | None, optional): Leave out fixes less accurate than this (meters).. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Track]
"""
        variables: dict[str, builtins.object] = {}
        variables['since'] = since
        variables['until'] = until
        if devices is not UNSET:
            variables['devices'] = devices
        if simplify is not UNSET:
            variables['simplify'] = simplify
        if max_accuracy is not UNSET:
            variables['maxAccuracy'] = max_accuracy
        return self.execute(GetRouteQuery, variables, task=task).route

    async def aget_stats(self, since: datetime, until: datetime, granularity: Granularity | None | UnsetType=UNSET, timezone: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[StatsBucket, ...]:
        """GetStats 
 Points, visits, trips and distance per day, week or month.

Args:
    since (datetime): No description
    until (datetime): No description
    granularity (Granularity | None, optional): No description. 
    timezone (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[StatsBucket]
"""
        variables: dict[str, builtins.object] = {}
        variables['since'] = since
        variables['until'] = until
        if granularity is not UNSET:
            variables['granularity'] = granularity
        if timezone is not UNSET:
            variables['timezone'] = timezone
        return (await self.aexecute(GetStatsQuery, variables, task=task)).stats

    def get_stats(self, since: datetime, until: datetime, granularity: Granularity | None | UnsetType=UNSET, timezone: str | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[StatsBucket, ...]:
        """GetStats 
 Points, visits, trips and distance per day, week or month.

Args:
    since (datetime): No description
    until (datetime): No description
    granularity (Granularity | None, optional): No description. 
    timezone (str | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[StatsBucket]
"""
        variables: dict[str, builtins.object] = {}
        variables['since'] = since
        variables['until'] = until
        if granularity is not UNSET:
            variables['granularity'] = granularity
        if timezone is not UNSET:
            variables['timezone'] = timezone
        return self.execute(GetStatsQuery, variables, task=task).stats

    async def aget_place_stats(self, since: datetime | None | UnsetType=UNSET, until: datetime | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[PlaceStat, ...]:
        """GetPlaceStats 
 Time spent per place, most first.

Args:
    since (datetime | None, optional): No description. 
    until (datetime | None, optional): No description. 
    limit (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[PlaceStat]
"""
        variables: dict[str, builtins.object] = {}
        if since is not UNSET:
            variables['since'] = since
        if until is not UNSET:
            variables['until'] = until
        if limit is not UNSET:
            variables['limit'] = limit
        return (await self.aexecute(GetPlaceStatsQuery, variables, task=task)).place_stats

    def get_place_stats(self, since: datetime | None | UnsetType=UNSET, until: datetime | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[PlaceStat, ...]:
        """GetPlaceStats 
 Time spent per place, most first.

Args:
    since (datetime | None, optional): No description. 
    until (datetime | None, optional): No description. 
    limit (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[PlaceStat]
"""
        variables: dict[str, builtins.object] = {}
        if since is not UNSET:
            variables['since'] = since
        if until is not UNSET:
            variables['until'] = until
        if limit is not UNSET:
            variables['limit'] = limit
        return self.execute(GetPlaceStatsQuery, variables, task=task).place_stats

    async def aget_sync_state(self, task: TaskLike | None=None) -> SyncState:
        """GetSyncState 
 The calling device's watermarks: its newest point, how many, and its last segment window.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    SyncState
"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(GetSyncStateQuery, variables, task=task)).sync_state

    def get_sync_state(self, task: TaskLike | None=None) -> SyncState:
        """GetSyncState 
 The calling device's watermarks: its newest point, how many, and its last segment window.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    SyncState
"""
        variables: dict[str, builtins.object] = {}
        return self.execute(GetSyncStateQuery, variables, task=task).sync_state

    async def aget_changes(self, cursor: str | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> ChangeSet:
        """GetChanges 
 One page of everything you have, from all your devices, changed after `cursor`. Page until hasMore is false.

Args:
    cursor (str | None, optional): No description. 
    limit (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ChangeSet
"""
        variables: dict[str, builtins.object] = {}
        if cursor is not UNSET:
            variables['cursor'] = cursor
        if limit is not UNSET:
            variables['limit'] = limit
        return (await self.aexecute(GetChangesQuery, variables, task=task)).changes

    def get_changes(self, cursor: str | None | UnsetType=UNSET, limit: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> ChangeSet:
        """GetChanges 
 One page of everything you have, from all your devices, changed after `cursor`. Page until hasMore is false.

Args:
    cursor (str | None, optional): No description. 
    limit (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    ChangeSet
"""
        variables: dict[str, builtins.object] = {}
        if cursor is not UNSET:
            variables['cursor'] = cursor
        if limit is not UNSET:
            variables['limit'] = limit
        return self.execute(GetChangesQuery, variables, task=task).changes

    async def alist_devices(self, filters: DeviceFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[DeviceOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailDevice, ...]:
        """ListDevices 
 Your phones (installs) that have backed up here.

Args:
    filters (DeviceFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[DeviceOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailDevice]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return (await self.aexecute(ListDevicesQuery, variables, task=task)).devices

    def list_devices(self, filters: DeviceFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[DeviceOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailDevice, ...]:
        """ListDevices 
 Your phones (installs) that have backed up here.

Args:
    filters (DeviceFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[DeviceOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailDevice]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return self.execute(ListDevicesQuery, variables, task=task).devices

    async def aget_device(self, id: IDCoercible, task: TaskLike | None=None) -> DetailDevice:
        """GetDevice 
 A device by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailDevice
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetDeviceQuery, variables, task=task)).device

    def get_device(self, id: IDCoercible, task: TaskLike | None=None) -> DetailDevice:
        """GetDevice 
 A device by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailDevice
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetDeviceQuery, variables, task=task).device

    async def alist_points(self, filters: PointFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[PointOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Point, ...]:
        """ListPoints 
 Location fixes, filterable by time, device, map box or radius.

Args:
    filters (PointFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[PointOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Point]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return (await self.aexecute(ListPointsQuery, variables, task=task)).points

    def list_points(self, filters: PointFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[PointOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Point, ...]:
        """ListPoints 
 Location fixes, filterable by time, device, map box or radius.

Args:
    filters (PointFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[PointOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Point]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return self.execute(ListPointsQuery, variables, task=task).points

    async def acount_points(self, filters: PointFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountPoints 
 How many points match.

Args:
    filters (PointFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return (await self.aexecute(CountPointsQuery, variables, task=task)).points_count

    def count_points(self, filters: PointFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountPoints 
 How many points match.

Args:
    filters (PointFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return self.execute(CountPointsQuery, variables, task=task).points_count

    async def aget_point(self, id: IDCoercible, task: TaskLike | None=None) -> Point:
        """GetPoint 
 A point by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Point
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetPointQuery, variables, task=task)).point

    def get_point(self, id: IDCoercible, task: TaskLike | None=None) -> Point:
        """GetPoint 
 A point by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Point
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetPointQuery, variables, task=task).point

    async def alist_visits(self, filters: VisitFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[VisitOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailVisit, ...]:
        """ListVisits 
 Stays, filterable by time, device, place, duration, map box or radius.

Args:
    filters (VisitFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[VisitOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailVisit]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return (await self.aexecute(ListVisitsQuery, variables, task=task)).visits

    def list_visits(self, filters: VisitFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[VisitOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailVisit, ...]:
        """ListVisits 
 Stays, filterable by time, device, place, duration, map box or radius.

Args:
    filters (VisitFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[VisitOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailVisit]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return self.execute(ListVisitsQuery, variables, task=task).visits

    async def acount_visits(self, filters: VisitFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountVisits 
 How many visits match.

Args:
    filters (VisitFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return (await self.aexecute(CountVisitsQuery, variables, task=task)).visits_count

    def count_visits(self, filters: VisitFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountVisits 
 How many visits match.

Args:
    filters (VisitFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return self.execute(CountVisitsQuery, variables, task=task).visits_count

    async def aget_visit(self, id: IDCoercible, task: TaskLike | None=None) -> DetailVisit:
        """GetVisit 
 A visit by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailVisit
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetVisitQuery, variables, task=task)).visit

    def get_visit(self, id: IDCoercible, task: TaskLike | None=None) -> DetailVisit:
        """GetVisit 
 A visit by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailVisit
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetVisitQuery, variables, task=task).visit

    async def alist_trips(self, filters: TripFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[TripOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Trip, ...]:
        """ListTrips 
 Movements between visits, filterable by time, device, mode or distance.

Args:
    filters (TripFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[TripOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Trip]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return (await self.aexecute(ListTripsQuery, variables, task=task)).trips

    def list_trips(self, filters: TripFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[TripOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[Trip, ...]:
        """ListTrips 
 Movements between visits, filterable by time, device, mode or distance.

Args:
    filters (TripFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[TripOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[Trip]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return self.execute(ListTripsQuery, variables, task=task).trips

    async def acount_trips(self, filters: TripFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountTrips 
 How many trips match.

Args:
    filters (TripFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return (await self.aexecute(CountTripsQuery, variables, task=task)).trips_count

    def count_trips(self, filters: TripFilter | None | UnsetType=UNSET, task: TaskLike | None=None) -> int:
        """CountTrips 
 How many trips match.

Args:
    filters (TripFilter | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    int
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        return self.execute(CountTripsQuery, variables, task=task).trips_count

    async def aget_trip(self, id: IDCoercible, task: TaskLike | None=None) -> Trip:
        """GetTrip 
 A trip by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Trip
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetTripQuery, variables, task=task)).trip

    def get_trip(self, id: IDCoercible, task: TaskLike | None=None) -> Trip:
        """GetTrip 
 A trip by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Trip
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetTripQuery, variables, task=task).trip

    async def alist_places(self, filters: PlaceFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[PlaceOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailPlace, ...]:
        """ListPlaces 
 Your named places, filterable by name, map box or radius.

Args:
    filters (PlaceFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[PlaceOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailPlace]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return (await self.aexecute(ListPlacesQuery, variables, task=task)).places

    def list_places(self, filters: PlaceFilter | None | UnsetType=UNSET, pagination: OffsetPaginationInput | None | UnsetType=UNSET, ordering: list[PlaceOrder] | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[DetailPlace, ...]:
        """ListPlaces 
 Your named places, filterable by name, map box or radius.

Args:
    filters (PlaceFilter | None, optional): No description. 
    pagination (OffsetPaginationInput | None, optional): No description. 
    ordering (list[PlaceOrder] | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[DetailPlace]
"""
        variables: dict[str, builtins.object] = {}
        if filters is not UNSET:
            variables['filters'] = filters
        if pagination is not UNSET:
            variables['pagination'] = pagination
        if ordering is not UNSET:
            variables['ordering'] = ordering
        return self.execute(ListPlacesQuery, variables, task=task).places

    async def aget_place(self, id: IDCoercible, task: TaskLike | None=None) -> DetailPlace:
        """GetPlace 
 A place by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailPlace
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return (await self.aexecute(GetPlaceQuery, variables, task=task)).place

    def get_place(self, id: IDCoercible, task: TaskLike | None=None) -> DetailPlace:
        """GetPlace 
 A place by id.

Args:
    id (ID): No description
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    DetailPlace
"""
        variables: dict[str, builtins.object] = {}
        variables['id'] = id
        return self.execute(GetPlaceQuery, variables, task=task).place
DeviceFilter.model_rebuild()
PlaceFilter.model_rebuild()
PointFilter.model_rebuild()
TripFilter.model_rebuild()
VisitFilter.model_rebuild()