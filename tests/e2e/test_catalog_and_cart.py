import pytest
from playwright.sync_api import Page, expect

from .helpers import add_to_cart

pytestmark = pytest.mark.e2e


def test_catalog_shows_products(page: Page):
    """TC-E2E-05"""
    page.goto("/")
    expect(page.get_by_role("heading", name="Products")).to_be_visible()
    expect(page.locator(".card")).not_to_have_count(0)


def test_category_filter(page: Page):
    """TC-E2E-06"""
    page.goto("/")
    page.get_by_role("link", name="Tea", exact=True).click()
    cards = page.locator(".card")
    expect(cards).not_to_have_count(0)
    for i in range(cards.count()):
        expect(cards.nth(i).locator("small")).to_have_text("Tea")


def test_add_to_cart_updates_counter_and_total(page: Page):
    """TC-E2E-07: 2 x 29.99 = 59.98 PLN"""
    add_to_cart(page, "Sencha green tea", quantity=2)
    expect(page.locator(".flash")).to_contain_text("Added to cart")
    expect(page.get_by_role("link", name="Cart (2)")).to_be_visible()
    page.get_by_role("link", name="Cart (2)").click()
    expect(page.get_by_text("Total: 59.98 PLN")).to_be_visible()


def test_remove_from_cart(page: Page):
    """TC-E2E-08"""
    add_to_cart(page, "Travel mug")
    page.goto("/cart")
    page.get_by_role("button", name="Remove").click()
    expect(page.get_by_text("Your cart is empty")).to_be_visible()
