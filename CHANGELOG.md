# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-13

### Added
- Initial release: one MCP server exposing **both** Google Analytics 4 and
  Google Tag Manager tools, authenticated by a single Google Cloud service
  account via `GOOGLE_APPLICATION_CREDENTIALS`.
- **GA4 read tools:** account/property discovery, property details, data
  streams, reports (`run_report`), realtime reports, and listing of custom
  dimensions, custom metrics, key events, and audiences.
- **GA4 write tools:** create and archive custom dimensions, create custom
  metrics, create key events (conversions), create and archive audiences,
  manage Measurement Protocol secrets, and send events via the Measurement
  Protocol.
- **GTM read tools:** list accounts, containers, workspaces, tags, triggers,
  variables; get a tag; list container versions; get the live version.
- **GTM write tools:** create/update/delete tags, triggers, and variables;
  create a container version; and publish a version to live (guarded by a
  `confirm` flag).
- Packaging as an installable console script (`google-analytics-gtm-mcp`).

[0.1.0]: https://github.com/burhan29ee/google-analytics-gtm-mcp/releases/tag/v0.1.0
