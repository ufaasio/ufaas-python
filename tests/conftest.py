"""Shared pytest fixtures for testing."""

import os

import dotenv
import pytest

dotenv.load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def setup_debugpy() -> None:
    """Set up debugpy for remote debugging."""
    if os.getenv("DEBUGPY", "False").lower() in ("true", "1", "yes"):
        import debugpy  # ruff:ignore[debugger]

        debugpy.listen(("127.0.0.1", 3020))  # ruff:ignore[debugger]
        debugpy.wait_for_client()  # ruff:ignore[debugger]
