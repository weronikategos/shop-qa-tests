"""Tests for known bugs. The reports are in docs/bugs.

Each test checks the CORRECT behaviour. Until the bug is fixed the test fails, so it is marked
xfail (expected failure). With strict=True, once someone fixes the bug the test starts passing
and pytest reports it, which is the signal to close the issue and remove the xfail.
"""
import uuid

import pytest
import requests

pytestmark = pytest.mark.known_bug


def registered_session(base_url, user):
    session = requests.Session()
    session.post(f"{base_url}/register", data=user)
    session.post(f"{base_url}/login", data={"email": user["email"], "password": user["password"]})
    return session


@pytest.mark.xfail(strict=True, reason="BUG-001: every logged-in customer can see the sales report")
def test_sales_report_is_not_available_to_regular_customer(api, new_user):
    session = registered_session(api.base_url, new_user)
    response = session.get(f"{api.base_url}/report", allow_redirects=False)
    assert response.status_code in (302, 403), "a regular customer should not see the whole shop's revenue"


@pytest.mark.xfail(strict=True, reason="BUG-002: the server accepts an invalid email address")
@pytest.mark.parametrize("pattern", ["{id}@", "@{id}.com", "{id}@@example.com"])
def test_server_rejects_invalid_email(api, new_user, pattern):
    bad_email = pattern.format(id=uuid.uuid4().hex[:8])  # unique, so we don't hit "already exists"
    # post the form directly, skipping the browser's validation (input type=email)
    response = requests.post(f"{api.base_url}/register",
                             data={**new_user, "email": bad_email}, allow_redirects=False)
    assert response.status_code != 302, f"an account with {bad_email!r} was created"
    assert "a valid email" in response.text
