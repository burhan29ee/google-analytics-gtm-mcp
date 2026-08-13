"""Smoke tests: the package imports and pure helpers work without credentials."""


def test_package_version():
    import google_analytics_gtm_mcp

    assert google_analytics_gtm_mcp.__version__


def test_server_and_entrypoint():
    from google_analytics_gtm_mcp import server

    assert callable(server.main)
    assert server.mcp is not None


def test_normalize_property_id():
    from google_analytics_gtm_mcp import server

    assert server._prop("123") == "properties/123"
    assert server._prop("properties/123") == "properties/123"
    assert server._prop("p123") == "properties/123"


def test_gtm_path_helpers():
    from google_analytics_gtm_mcp import server

    assert server._acc("1") == "accounts/1"
    assert server._cont("1", "2") == "accounts/1/containers/2"
    assert server._ws("1", "2", "3") == "accounts/1/containers/2/workspaces/3"
