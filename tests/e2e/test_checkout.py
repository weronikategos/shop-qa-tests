import re

import pytest
from playwright.sync_api import Page, expect

from .helpers import add_to_cart, login, register

pytestmark = pytest.mark.e2e

PRODUCT = "Colombia ground coffee"


def product_by_name(api, name):
    return next(p for p in api.get(f"{api.base_url}/api/products").json() if p["name"].startswith(name))


def test_checkout_requires_login(page: Page):
    """TC-E2E-09: a guest is redirected to the login page"""
    add_to_cart(page, PRODUCT)
    page.goto("/cart")
    page.get_by_role("button", name="Place order").click()
    expect(page).to_have_url(re.compile(r".*/login"))
    expect(page.locator(".flash")).to_contain_text("Please log in")


def test_full_order_decreases_stock(page: Page, api, new_user):
    """TC-E2E-10: the order is saved and stock goes down by exactly the ordered quantity"""
    stock_before = product_by_name(api, PRODUCT)["stock"]
    register(page, new_user)
    login(page, new_user)
    add_to_cart(page, PRODUCT, quantity=2)
    page.goto("/cart")
    page.get_by_role("button", name="Place order").click()

    expect(page.get_by_role("heading", name="Order #")).to_be_visible()
    expect(page.get_by_text("Total: 69.98 PLN")).to_be_visible()  # 2 x 34.99
    assert product_by_name(api, PRODUCT)["stock"] == stock_before - 2

    page.get_by_role("link", name="My orders").click()
    expect(page.locator("table tr")).to_have_count(2)  # header + one order


def test_cannot_add_more_than_stock(page: Page, api):
    """TC-E2E-11: boundary value, stock + 1"""
    product = product_by_name(api, "Hand coffee grinder")
    page.goto("/")
    card = page.locator(".card").filter(has_text="Hand coffee grinder")
    # remove the browser-side limit (the max attribute) to check the server-side validation
    card.locator("input[name=quantity]").evaluate("el => el.removeAttribute('max')")
    card.locator("input[name=quantity]").fill(str(product["stock"] + 1))
    card.get_by_role("button", name="Add to cart").click()
    expect(page.locator(".flash")).to_contain_text("have that many in stock")
