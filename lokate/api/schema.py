import builtins
from datetime import datetime
from enum import Enum
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from rath.scalars import ID
from rath.task import TaskLike
from typing import Literal

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

class TripMode(str, Enum):
    """How a trip was travelled, as the phone classified it."""
    WALK = 'WALK'
    BIKE = 'BIKE'
    VEHICLE = 'VEHICLE'
    UNKNOWN = 'UNKNOWN'
    __str__ = str.__str__

class DeletedInput(BaseModel):
    """No documentation"""
    client_id: ID = Field(validation_alias=AliasChoices('client_id', 'clientId'), serialization_alias='clientId')
    deleted_at: datetime = Field(validation_alias=AliasChoices('deleted_at', 'deletedAt'), serialization_alias='deletedAt')
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

class AccessLogEntry(BaseModel):
    """One read of your data."""
    typename: Literal['AccessLogEntry'] = Field(alias='__typename', default='AccessLogEntry', exclude=True)
    id: ID
    operation: str
    range: str
    rows: int
    at: datetime
    device_id: str | None = Field(default=None, alias='deviceId')
    "The reading token's client_device claim."
    client_id: str | None = Field(default=None, alias='clientId')
    "The reading token's OAuth client."
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for AccessLogEntry"""
        document = 'fragment AccessLogEntry on AccessLogEntry {\n  id\n  operation\n  range\n  rows\n  at\n  deviceId\n  clientId\n  __typename\n}'
        name = 'AccessLogEntry'
        type = 'AccessLogEntry'

class Retention(BaseModel):
    """How long the server keeps your points and segments."""
    typename: Literal['Retention'] = Field(alias='__typename', default='Retention', exclude=True)
    days: int | None = Field(default=None)
    'Null: forever.'
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Retention"""
        document = 'fragment Retention on Retention {\n  days\n  __typename\n}'
        name = 'Retention'
        type = 'Retention'

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

class Point(BaseModel):
    """One location fix."""
    typename: Literal['Point'] = Field(alias='__typename', default='Point', exclude=True)
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    'The device (token client_device) that recorded it.'
    ts: datetime
    lat: float
    lon: float
    acc: float | None = Field(default=None)
    speed: float | None = Field(default=None)
    heading: float | None = Field(default=None)
    alt: float | None = Field(default=None)
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Point"""
        document = 'fragment Point on Point {\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}'
        name = 'Point'
        type = 'Point'

class Visit(BaseModel):
    """A stay at one spot."""
    typename: Literal['Visit'] = Field(alias='__typename', default='Visit', exclude=True)
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    start: datetime
    end: datetime
    lat: float
    lon: float
    radius: float
    point_count: int = Field(alias='pointCount')
    place_client_id: ID | None = Field(default=None, alias='placeClientId')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Visit"""
        document = 'fragment Visit on Visit {\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  __typename\n}'
        name = 'Visit'
        type = 'Visit'

class Trip(BaseModel):
    """A movement between two visits."""
    typename: Literal['Trip'] = Field(alias='__typename', default='Trip', exclude=True)
    client_id: ID = Field(alias='clientId')
    device_id: ID = Field(alias='deviceId')
    start: datetime
    end: datetime
    from_visit: ID | None = Field(default=None, alias='fromVisit')
    to_visit: ID | None = Field(default=None, alias='toVisit')
    distance: float
    mode: TripMode
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Trip"""
        document = 'fragment Trip on Trip {\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  __typename\n}'
        name = 'Trip'
        type = 'Trip'

class Place(BaseModel):
    """A named place, shared by all of a user's phones. A tombstone has deletedAt set and nothing else but its key."""
    typename: Literal['Place'] = Field(alias='__typename', default='Place', exclude=True)
    client_id: ID = Field(alias='clientId')
    name: str | None = Field(default=None)
    lat: float | None = Field(default=None)
    lon: float | None = Field(default=None)
    radius: float | None = Field(default=None)
    updated_at: datetime = Field(alias='updatedAt')
    deleted_at: datetime | None = Field(default=None, alias='deletedAt')
    model_config = ConfigDict(frozen=True)

    class Meta:
        """Meta class for Place"""
        document = 'fragment Place on Place {\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}'
        name = 'Place'
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
        document = 'fragment Place on Place {\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceSyncResult on PlaceSyncResult {\n  applied\n  stale {\n    ...Place\n    __typename\n  }\n  __typename\n}'
        name = 'PlaceSyncResult'
        type = 'PlaceSyncResult'

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
        document = 'fragment Place on Place {\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Point on Point {\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nfragment Trip on Trip {\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  __typename\n}\n\nfragment Visit on Visit {\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  __typename\n}\n\nfragment ChangeSet on ChangeSet {\n  points {\n    ...Point\n    __typename\n  }\n  visits {\n    ...Visit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  places {\n    ...Place\n    __typename\n  }\n  deletedPlaces\n  nextCursor\n  hasMore\n  __typename\n}'
        name = 'ChangeSet'
        type = 'ChangeSet'

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

class SetRetentionMutation(BaseModel):
    """ Keep your points and segments this many days (None: forever)."""
    set_retention: Retention = Field(alias='setRetention')
    'Keep your points and segments this many days (null: forever). Older ones are deleted now and on every later upload.'

    class Arguments(BaseModel):
        """Arguments for SetRetention """
        days: int | None = Field(default=None)

    class Meta:
        """Meta class for SetRetention """
        document = 'fragment Retention on Retention {\n  days\n  __typename\n}\n\nmutation SetRetention($days: Int) {\n  setRetention(days: $days) {\n    ...Retention\n    __typename\n  }\n}'

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
        document = 'fragment Place on Place {\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment PlaceSyncResult on PlaceSyncResult {\n  applied\n  stale {\n    ...Place\n    __typename\n  }\n  __typename\n}\n\nmutation MergePlaces($places: [PlaceInput!]!, $deleted: [DeletedInput!]!) {\n  syncPlaces(places: $places, deleted: $deleted) {\n    ...PlaceSyncResult\n    __typename\n  }\n}'

class ListAccessLogQuery(BaseModel):
    """ Every read of your data, newest first."""
    access_log: tuple[AccessLogEntry, ...] = Field(alias='accessLog')
    'Every read of your data, newest first.'

    class Arguments(BaseModel):
        """Arguments for ListAccessLog """
        limit: int | None = Field(default=None)
        offset: int | None = Field(default=None)

    class Meta:
        """Meta class for ListAccessLog """
        document = 'fragment AccessLogEntry on AccessLogEntry {\n  id\n  operation\n  range\n  rows\n  at\n  deviceId\n  clientId\n  __typename\n}\n\nquery ListAccessLog($limit: Int, $offset: Int) {\n  accessLog(limit: $limit, offset: $offset) {\n    ...AccessLogEntry\n    __typename\n  }\n}'

class GetRetentionQuery(BaseModel):
    """ How long the server keeps your points and segments."""
    retention: Retention
    'How long the server keeps your points and segments.'

    class Arguments(BaseModel):
        """Arguments for GetRetention """
        pass

    class Meta:
        """Meta class for GetRetention """
        document = 'fragment Retention on Retention {\n  days\n  __typename\n}\n\nquery GetRetention {\n  retention {\n    ...Retention\n    __typename\n  }\n}'

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
    "Everything of the user's, from all their devices, changed after `cursor`, oldest first (limit at most 1000). Page until hasMore is false; used to restore."

    class Arguments(BaseModel):
        """Arguments for GetChanges """
        cursor: str | None = Field(default=None)
        limit: int | None = Field(default=None)

    class Meta:
        """Meta class for GetChanges """
        document = 'fragment Place on Place {\n  clientId\n  name\n  lat\n  lon\n  radius\n  updatedAt\n  deletedAt\n  __typename\n}\n\nfragment Point on Point {\n  clientId\n  deviceId\n  ts\n  lat\n  lon\n  acc\n  speed\n  heading\n  alt\n  __typename\n}\n\nfragment Trip on Trip {\n  clientId\n  deviceId\n  start\n  end\n  fromVisit\n  toVisit\n  distance\n  mode\n  __typename\n}\n\nfragment Visit on Visit {\n  clientId\n  deviceId\n  start\n  end\n  lat\n  lon\n  radius\n  pointCount\n  placeClientId\n  __typename\n}\n\nfragment ChangeSet on ChangeSet {\n  points {\n    ...Point\n    __typename\n  }\n  visits {\n    ...Visit\n    __typename\n  }\n  trips {\n    ...Trip\n    __typename\n  }\n  places {\n    ...Place\n    __typename\n  }\n  deletedPlaces\n  nextCursor\n  hasMore\n  __typename\n}\n\nquery GetChanges($cursor: String, $limit: Int) {\n  changes(cursor: $cursor, limit: $limit) {\n    ...ChangeSet\n    __typename\n  }\n}'

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

    async def aset_retention(self, days: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> Retention:
        """SetRetention 
 Keep your points and segments this many days (None: forever).

Args:
    days (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Retention
"""
        variables: dict[str, builtins.object] = {}
        if days is not UNSET:
            variables['days'] = days
        return (await self.aexecute(SetRetentionMutation, variables, task=task)).set_retention

    def set_retention(self, days: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> Retention:
        """SetRetention 
 Keep your points and segments this many days (None: forever).

Args:
    days (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Retention
"""
        variables: dict[str, builtins.object] = {}
        if days is not UNSET:
            variables['days'] = days
        return self.execute(SetRetentionMutation, variables, task=task).set_retention

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

    async def alist_access_log(self, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[AccessLogEntry, ...]:
        """ListAccessLog 
 Every read of your data, newest first.

Args:
    limit (int | None, optional): No description. 
    offset (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[AccessLogEntry]
"""
        variables: dict[str, builtins.object] = {}
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return (await self.aexecute(ListAccessLogQuery, variables, task=task)).access_log

    def list_access_log(self, limit: int | None | UnsetType=UNSET, offset: int | None | UnsetType=UNSET, task: TaskLike | None=None) -> tuple[AccessLogEntry, ...]:
        """ListAccessLog 
 Every read of your data, newest first.

Args:
    limit (int | None, optional): No description. 
    offset (int | None, optional): No description. 
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    list[AccessLogEntry]
"""
        variables: dict[str, builtins.object] = {}
        if limit is not UNSET:
            variables['limit'] = limit
        if offset is not UNSET:
            variables['offset'] = offset
        return self.execute(ListAccessLogQuery, variables, task=task).access_log

    async def aget_retention(self, task: TaskLike | None=None) -> Retention:
        """GetRetention 
 How long the server keeps your points and segments.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Retention
"""
        variables: dict[str, builtins.object] = {}
        return (await self.aexecute(GetRetentionQuery, variables, task=task)).retention

    def get_retention(self, task: TaskLike | None=None) -> Retention:
        """GetRetention 
 How long the server keeps your points and segments.

Args:
    task (rath.task.TaskLike, optional): The task this call is made for; the ambient one by default.

Returns:
    Retention
"""
        variables: dict[str, builtins.object] = {}
        return self.execute(GetRetentionQuery, variables, task=task).retention

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