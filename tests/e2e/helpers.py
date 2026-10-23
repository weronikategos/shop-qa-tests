"""Steps shared by many E2E tests."""
from playwright.sync_api import Page


def register(page: Page, user: dict) -> None:
    page.goto("/register")
    page.get_by_label("Name").fill(user["name"])
    page.get_by_label("Email").fill(user["email"])
    page.get_by_label("Password").fill(user["password"])
    page.get_by_role("button", name="Sign up").click()


def login(page: Page, user: dict) -> None:
    page.goto("/login")
    page.get_by_label("Email").fill(user["email"])
    page.get_by_label("Password").fill(user["password"])
    page.get_by_role("button", name="Log in").click()


def add_to_cart(page: Page, product_name: str, quantity: int = 1) -> None:
    page.goto("/")
    card = page.locator(".card").filter(has_text=product_name)
    card.locator("input[name=quantity]").fill(str(quantity))
    card.get_by_role("button", name="Add to cart").click()
