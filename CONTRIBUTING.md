# Contributing

Thanks for your interest in improving **google-analytics-gtm-mcp**!
Contributions of all kinds are welcome — bug reports, feature requests, docs,
and code.

## Development setup

Requires Python 3.10+.

```bash
git clone https://github.com/burhan29ee/google-analytics-gtm-mcp.git
cd google-analytics-gtm-mcp
python -m venv .venv && source .venv/bin/activate   # or: uv venv --python 3.12 .venv
pip install -e ".[dev]"                              # installs the package + pytest + ruff
```

## Running checks

```bash
ruff check .     # lint
pytest -q        # tests
```

The smoke tests import the package and exercise pure helpers — they do **not**
require Google credentials.

## Testing against live GA4 / GTM (optional)

For manual end-to-end testing, point the server at a service-account key that
has access to a GA4 property and a GTM container, and try tools against a
throwaway/scratch property and container. Always archive or delete anything a
write tool creates. For GA4 events use `send_ga4_event(..., validate=True)` so
payloads are checked without being ingested, and for GTM never call
`gtm_publish_version` against a production container while testing.

## Pull requests

1. Open an issue first for anything non-trivial so we can agree on the approach.
2. Keep changes focused; add or update a test when it makes sense.
3. Run `ruff check .` and `pytest` before pushing.
4. Update `CHANGELOG.md` under an "Unreleased" heading.
5. Never commit credentials — the `.gitignore` blocks key files, `.env`, and
   `*.json` (except the example config).

## Notes for maintainers

- The `mcp` dependency is pinned to `>=1.2,<2`: the 2.0 SDK reorganized its API
  and removed `mcp.server.fastmcp`, which this server uses.
- Client construction is lazy so the package imports without credentials.
- GA4 uses the `google-analytics-data` / `google-analytics-admin` client
  libraries; audiences use the Admin **v1alpha** surface. GTM uses the
  `google-api-python-client` discovery client for Tag Manager **v2**.
- GA4 and GTM use different OAuth scopes on the same key, so the two client
  factories build separate credentials from the one JSON file.
