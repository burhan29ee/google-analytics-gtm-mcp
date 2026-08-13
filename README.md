# google-analytics-gtm-mcp

[![CI](https://github.com/burhan29ee/google-analytics-gtm-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/burhan29ee/google-analytics-gtm-mcp/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

One [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for **Google Analytics 4** *and* **Google Tag Manager**, with both **read and write** access. Connect it to Claude (or any MCP client) and, in natural language, pull GA4 reports, manage measurement configuration, build remarketing audiences, and edit and publish GTM tags, triggers, and variables — all with your own Google credentials. No third-party service, no subscription.

A single Google Cloud **service account** powers both surfaces: grant it access in Google Analytics and in Tag Manager, point one environment variable at its key, and you get **40 tools** across the two products from one server entry.

## Features

**Google Analytics 4 — read**
- List accounts and properties, property details, and data streams
- Run GA4 reports (`run_report`) and realtime reports (`run_realtime_report`)
- List custom dimensions, custom metrics, key events (conversions), and audiences

**Google Analytics 4 — write**
- Create and archive custom dimensions; create custom metrics
- Create key events (conversions)
- Create and archive **audiences** (remarketing lists you can share to Google Ads)
- Create / list / delete **Measurement Protocol** API secrets
- **Send events** via the Measurement Protocol (with a `validate=True` mode that checks a payload without ingesting it)

**Google Tag Manager — read**
- List accounts, containers, workspaces, tags, triggers, and variables
- Get a single tag; list container versions; get the live (published) version

**Google Tag Manager — write**
- Create, update, and delete **tags**, **triggers**, and **variables**
- Create a container **version** from a workspace
- **Publish** a version to live (guarded by `confirm=true`)

## Requirements

- **Python 3.10+** (the MCP SDK requires it)
- A Google Cloud project and a **service account** with a JSON key
- The service account granted access on your **GA4** account/property *and* your **GTM** account/container

## Google setup (one time)

1. In the [Google Cloud Console](https://console.cloud.google.com), create (or pick) a project.
2. Enable three APIs for that project: **Google Analytics Data API**, **Google Analytics Admin API**, and **Tag Manager API**.
3. Create a **service account** and download a **JSON key** for it. Note its email (`...@your-project.iam.gserviceaccount.com`).
4. In **Google Analytics → Admin → Account (or Property) access management**, add that email as a user — **Editor** if you want write access, Viewer/Analyst for read-only.
5. In **Tag Manager → Admin → User Management** (at the account and/or container level), add the same email — grant **Publish** (container permission) if you want to create and publish versions, or **Read** for read-only.

That's it — no OAuth consent screen, no token refresh. The service account authenticates directly.

## Install

Using [uv](https://docs.astral.sh/uv/) (recommended — it manages an isolated Python for you):

```bash
git clone https://github.com/burhan29ee/google-analytics-gtm-mcp.git
cd google-analytics-gtm-mcp
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e .
```

Or with pip:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Configure your MCP client

Point the server at your service-account key with the `GOOGLE_APPLICATION_CREDENTIALS` environment variable, then add it to your client. For **Claude Desktop**, edit `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`; Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google-analytics-gtm": {
      "command": "/absolute/path/to/google-analytics-gtm-mcp/.venv/bin/python",
      "args": ["-m", "google_analytics_gtm_mcp.server"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/absolute/path/to/service-account-key.json"
      }
    }
  }
}
```

Restart the client. You should be able to ask things like *"list my GA4 properties,"* *"pull last 28 days of users and conversions by channel,"* *"create a remarketing audience of everyone who fired generate_lead in the last 60 days,"* or *"list the tags in my GTM container and show me the live version."*

## Tool reference

### Google Analytics 4

| Tool | Type | What it does |
|------|------|--------------|
| `list_account_summaries` | read | List accounts and their properties |
| `get_property_details` | read | Property name, time zone, currency, industry |
| `list_data_streams` | read | Web/app streams and their measurement IDs |
| `run_report` | read | GA4 report by metrics/dimensions/date range |
| `run_realtime_report` | read | Realtime report (last ~30 min) |
| `list_custom_dimensions` | read | Custom dimensions on a property |
| `create_custom_dimension` | write | Create a custom dimension |
| `archive_custom_dimension` | write | Archive a custom dimension |
| `list_custom_metrics` | read | Custom metrics on a property |
| `create_custom_metric` | write | Create a custom metric |
| `list_key_events` | read | Key events (conversions) |
| `create_key_event` | write | Mark an event as a conversion |
| `list_audiences` | read | Audiences on a property |
| `create_event_audience` | write | Create an audience of users who fired an event |
| `archive_audience` | write | Archive an audience |
| `list_measurement_protocol_secrets` | read | MP API secrets for a stream |
| `create_measurement_protocol_secret` | write | Create an MP API secret |
| `delete_measurement_protocol_secret` | write | Delete an MP API secret |
| `send_ga4_event` | write | Send an event via the Measurement Protocol |

### Google Tag Manager

| Tool | Type | What it does |
|------|------|--------------|
| `gtm_whoami` | read | Show the service-account identity, scopes, and visible accounts |
| `gtm_list_accounts` | read | List GTM accounts |
| `gtm_list_containers` | read | List containers in an account |
| `gtm_list_workspaces` | read | List workspaces in a container |
| `gtm_list_tags` | read | List tags in a workspace |
| `gtm_list_triggers` | read | List triggers in a workspace |
| `gtm_list_variables` | read | List variables in a workspace |
| `gtm_get_tag` | read | Get a single tag by id |
| `gtm_list_versions` | read | List container version headers |
| `gtm_get_live_version` | read | Get the live (published) version |
| `gtm_create_tag` | write | Create a tag from a JSON resource |
| `gtm_update_tag` | write | Update an existing tag |
| `gtm_delete_tag` | write | Delete a tag (`confirm=true`) |
| `gtm_create_trigger` | write | Create a trigger |
| `gtm_update_trigger` | write | Update a trigger |
| `gtm_delete_trigger` | write | Delete a trigger (`confirm=true`) |
| `gtm_create_variable` | write | Create a variable |
| `gtm_update_variable` | write | Update a variable |
| `gtm_delete_variable` | write | Delete a variable (`confirm=true`) |
| `gtm_create_version` | write | Freeze a workspace into a new version |
| `gtm_publish_version` | write | Publish a version to live (`confirm=true`) |

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest -q
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## Security

The service-account key is a credential — treat it like a password. Never commit it (the `.gitignore` blocks key files), grant the service account the least access it needs in each product, and rotate the key if it's ever exposed. GTM write tools that affect a live container (`gtm_delete_*`, `gtm_publish_version`) require `confirm=true`. See [SECURITY.md](SECURITY.md) for details and how to report a vulnerability.

## Notes

- The `mcp` dependency is pinned to `>=1.2,<2`. The 2.0 SDK reorganized its API and removed `mcp.server.fastmcp`, which this server uses.
- GA4 audiences use the GA4 Admin **v1alpha** API; the rest of GA4 uses the stable v1beta and Data APIs. GTM uses the Tag Manager **v2** API.
- This is an independent open-source project and is not affiliated with or endorsed by Google.

## License

[MIT](LICENSE)
