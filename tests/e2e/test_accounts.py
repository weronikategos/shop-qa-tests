import pytest
from playwright.sync_api import Page, expect

from .helpers import login, register

pytestmark = pytest.mark.e2e


def test_register_and_login(page: Page, new_user):
    """TC-E2E-01: a new customer signs up and logs in"""
    register(page, new_user)
    expect(page.locator(".flash")).to_contain_text("Account created")
    login(page, new_user)
    expect(page.locator("nav")).to_contain_text(new_user["name"])
    expect(page.get_by_role("link", name="Log out")).to_be_visible()


def test_register_with_existing_email_shows_error(page: Page, new_user):
    """TC-E2E-02"""
    register(page, new_user)
    register(page, new_user)
    expect(page.locator(".flash")).to_contain_text("already exists")


def test_login_with_wrong_password(page: Page, new_user):
    """TC-E2E-03"""
    register(page, new_user)
    login(page, {**new_user, "password": "wrong-password-123"})
    expect(page.locator(".flash")).to_contain_text("Invalid email or password")
    expect(page.get_by_role("link", name="Log in")).to_be_visible()


def test_logout(page: Page, new_user):
    """TC-E2E-04"""
    register(page, new_user)
    login(page, new_user)
    page.get_by_role("link", name="Log out").click()
    expect(page.get_by_role("link", name="Log in")).to_be_visible()
