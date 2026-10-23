# Test cases

The **Automated** column shows which automated test covers each case.

## Customer account

| ID | Title | Steps | Expected result | Severity | Automated |
|---|---|---|---|---|---|
| TC-E2E-01 | Sign up and log in | 1. Open "Sign up". 2. Enter a name, a new email and a password with 8+ characters. 3. Log in with these details. | Message "Account created"; after login the menu shows the name and "Log out" | critical | `test_register_and_login` |
| TC-E2E-02 | Sign up with an existing email | Create an account, then another one with the same email | Message "An account with this email already exists." | high | `test_register_with_existing_email_shows_error` |
| TC-E2E-03 | Log in with a wrong password | Log in with an existing email and a wrong password | Message "Invalid email or password.", customer stays logged out | high | `test_login_with_wrong_password` |
| TC-E2E-04 | Log out | Log in, click "Log out" | The menu shows "Log in" again | medium | `test_logout` |
| TC-M-01 | Invalid email sent past the browser | Submit the sign-up form with the email `ala@` (e.g. with Postman or by removing `type=email` in DevTools) | The server rejects the address | medium | `test_server_rejects_invalid_email` (**BUG-002**) |

## Catalog and cart

| ID | Title | Steps | Expected result | Severity | Automated |
|---|---|---|---|---|---|
| TC-E2E-05 | Catalog is shown | Open the home page | Heading "Products" and at least one product card | critical | `test_catalog_shows_products` |
| TC-E2E-06 | Category filter | Click "Tea" | Only products from the Tea category are shown | medium | `test_category_filter` |
| TC-E2E-07 | Add to cart | Add 2 × Sencha green tea | Counter "Cart (2)", the cart shows "Total: 59.98 PLN" | critical | `test_add_to_cart_updates_counter_and_total` |
| TC-E2E-08 | Remove from cart | Add a product, click "Remove" in the cart | "Your cart is empty" | medium | `test_remove_from_cart` |
| TC-E2E-11 | More items than in stock | Remove the `max` attribute from the quantity field and enter stock + 1 | Message "We don't have that many in stock." | high | `test_cannot_add_more_than_stock` |

## Orders

| ID | Title | Steps | Expected result | Severity | Automated |
|---|---|---|---|---|---|
| TC-E2E-09 | Checkout without logging in | As a guest, add a product and click "Place order" | Redirect to the login page with "Please log in to continue." | high | `test_checkout_requires_login` |
| TC-E2E-10 | Full order | Log in, add 2 × Colombia ground coffee, place the order | Page "Order #…", total 69.98 PLN, stock lower by 2, order listed in "My orders" | critical | `test_full_order_decreases_stock` |
| TC-M-02 | Sales report for a regular customer | Log in as a regular customer and open `/report` | Access denied (admins only) | high | `test_sales_report_is_not_available_to_regular_customer` (**BUG-001**) |

## API

| ID | Title | Expected result | Automated |
|---|---|---|---|
| TC-API-01 | `GET /api/health` | 200, `{"status": "ok"}` | `test_health_returns_ok` |
| TC-API-02 | Health response time | under 500 ms | `test_health_responds_quickly` |
| TC-API-03–06 | `GET /api/products` | non-empty list, fields and types match the contract, prices > 0, stock ≥ 0, unique ids | `tests/api/test_products.py` |
| TC-API-07 | Filter `?category=ID` | only products from that category | `test_filter_by_category_returns_only_that_category` |
| TC-API-08 | Category that doesn't exist | 200 and an empty list | `test_filter_with_unknown_category_returns_empty_list` |
| TC-API-09 | `?category=abc`, `-1`, `1.5`, empty | 400 and an `error` field | `test_filter_with_invalid_category_returns_400` |
| TC-API-10 | `GET /api/products/ID` | the same product as in the list | `test_single_product_matches_list` |
| TC-API-11 | Product that doesn't exist | 404 as JSON | `test_missing_product_returns_404_json` |

## Database (SQL)

| ID | Check | Automated |
|---|---|---|
| TC-DB-01 | no negative stock | `test_no_negative_stock` |
| TC-DB-02 | order total = sum of its items | `test_order_total_equals_sum_of_items` |
| TC-DB-03 | no empty orders | `test_every_order_has_items` |
| TC-DB-04 | no orphan order items | `test_no_orphan_rows` |
| TC-DB-05 | emails unique regardless of letter case | `test_emails_unique_case_insensitive` |
| TC-DB-06 | passwords stored only as hashes | `test_passwords_are_hashed` |
