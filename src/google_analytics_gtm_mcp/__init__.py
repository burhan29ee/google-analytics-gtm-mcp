"""google-analytics-gtm-mcp: one MCP server for Google Analytics 4 and Google
Tag Manager, with read and write access."""

from .server import main, mcp

__all__ = ["main", "mcp"]
__version__ = "0.1.0"
