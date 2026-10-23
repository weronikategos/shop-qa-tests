import os
import sqlite3
import uuid

import pytest
import requests


@pytest.fixture(scope="session")
def api(base_url):
    """HTTP session for the shop API. Stops the run early if the shop isn't up."""
    session = requests.Session()
    session.base_url = base_url.rstrip("/")
    try:
        session.get(f"{session.base_url}/api/health", timeout=5).raise_for_status()
    except requests.RequestException as exc:
        pytest.exit(f"The shop is not responding at {base_url}. Start it before running the tests. ({exc})")
    return session


@pytest.fixture
def new_user():
    """Unique customer details, so tests don't get in each other's way."""
    suffix = uuid.uuid4().hex[:8]
    return {"name": "Tester", "email": f"tester-{suffix}@example.com", "password": "test-password-1"}


@pytest.fixture
def db():
    """Read-only connection to the shop database. Set SHOP_DB to the path of shop.db."""
    path = os.environ.get("SHOP_DB")
    if not path:
        pytest.skip("Set SHOP_DB to the path of a shop.db file to run the database tests")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    yield conn
    conn.close()
