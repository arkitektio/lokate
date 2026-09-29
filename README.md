# lokate

The python client for [lokate](https://github.com/arkitektio/lokate-server), the
[Arkitekt](https://arkitekt.live) backup of a phone's location timeline: points,
visits, trips and places, uploaded idempotently and restorable page by page.

## Installation

```sh
pip install lokate
```

## Usage

Every lokate operation is a method of the `Lokate` client, in a blocking and an
`a`-prefixed async flavour. The server keys everything by the token's user and
writes by its device (`client_device` claim).

### In an arkitekt app

The client is injected by annotation. Add the service to your app and ask for
`lokate: Lokate`:

```python
from arkitekt import App, run
from lokate import Lokate, lokate_service

app = App("where-was-i", "0.1.0", services=[lokate_service])


@app.action
async def places_i_keep(lokate: Lokate) -> list[str]:
    """The names of my places, from the server copy."""
    names, cursor = [], None
    while True:
        page = await lokate.aget_changes(cursor=cursor)
        names += [place.name for place in page.places]
        cursor = page.next_cursor
        if not page.has_more:
            return names


if __name__ == "__main__":
    run(app)
```

### From a script

```python
from arkitekt import easy
from lokate import lokate_service

with easy("my-script", lokate_service) as lokate:
    state = lokate.get_sync_state()
    print(state.point_count, state.last_point_ts)
```

### Standalone

Without arkitekt, build the client over a rath link of your own:

```python
import datetime
from lokate import Lokate
from lokate.api.schema import PointInput
from lokate.rath import LokateRath

lokate = Lokate(rath=LokateRath(link=...))

with lokate:
    result = lokate.upload_points([
        PointInput(client_id="fix-1", ts=datetime.datetime.now(datetime.UTC), lat=48.2, lon=16.37),
    ])
    print(result.accepted, result.duplicates)
```

What the protocol guarantees:

- **Every write can be retried.** `upload_points` counts points it already has as
  `duplicates`. `replace_segments(from_=...)` and `merge_places` leave unchanged
  rows alone.
- **A point is keyed by `(device, client_id, ts)`.** Never send one `client_id`
  with two different timestamps.
- **Batches hold at most 1000 rows**, and so does a `get_changes` page.
- **Leave defaulted arguments out** rather than passing `None`. For `set_retention`,
  though, `days=None` is meaningful: it means keep forever.

## Development

The generated API (`lokate/api/schema.py`) comes from the checked-in
`schema.graphql` and the documents in `graphql/`. The config comment in
`graphql.config.yaml` has the command that refreshes the schema from a
lokate-server checkout. Then regenerate with turms:

```sh
uvx --with 'graphql-core<3.3' --with-editable . --from <path to turms> turms gen
```

```sh
uv run pytest -m "not integration"   # no server needed
uv run pytest -m integration          # a real lokate + postgres/PostGIS via dokker
```

Until the server's first image is published, the integration suite needs a
gitignored `tests/integration/docker-compose.local.yml` that builds
`jhnnsrs/lokate` from a local lokate-server checkout.

See [RELEASING.md](RELEASING.md) for how versions are cut.
