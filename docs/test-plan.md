# Test plan: Flask SQL Shop

## 1. Goal
Check that the online shop [flask-sql-shop](https://github.com/weronikategos/flask-sql-shop) handles the main customer journeys correctly (account, catalog, cart, checkout) and that the data in its database stays consistent.

## 2. Scope

| In scope | Out of scope |
|---|---|
| sign-up, login, logout | payments (the shop has none) |
| catalog and category filter | load testing |
| cart: adding, removing, stock limits | cross-browser checks (only Chromium is tested) |
| checkout and stock updates | security testing beyond basic access control |
| REST API: `/api/health`, `/api/categories`, `/api/products` | |
| data consistency in the SQLite database | |

## 3. Test types and tools

| Type | Tool | Where |
|---|---|---|
| manual (exploratory) tests | browser, DevTools | [test-cases.md](test-cases.md) |
| API tests | pytest + requests, Postman/newman | `tests/api`, `postman/` |
| E2E tests | Playwright (Python) | `tests/e2e` |
| data tests | SQL (SQLite, read-only) | `tests/db` |
| regression | GitHub Actions: on every push and every morning | `.github/workflows/qa.yml` |

## 4. Test design techniques
- **Equivalence partitioning:** valid / invalid category id (number, text, decimal, empty).
- **Boundary values:** ordering exactly the stock and stock + 1; a category that doesn't exist.
- **State transition testing:** guest → logged-in customer → logged out.
- **Negative tests:** wrong password, existing email, invalid email sent past the browser's validation.

## 5. Environment
The shop runs in Docker (`docker compose up`) at `http://localhost:8000`, with demo data (`flask demo-data`). Browser: Chromium (Playwright).

## 6. Entry and exit criteria
- **Entry:** the shop starts and `/api/health` returns `{"status": "ok"}`.
- **Exit:** all critical tests pass; every bug found has a report in `docs/bugs` and a GitHub issue.

## 7. Bug severity
| Severity | Meaning |
|---|---|
| critical | data loss, data leak, checkout impossible |
| high | an important feature works incorrectly, but there is a workaround |
| medium | validation error, wrong message |
| low | typo, cosmetic issue |

## 8. Risks
- E2E tests change the stock. That's why they read the stock before and after an order instead of assuming fixed numbers.
- Tests sign up new accounts with random emails, so they can be run many times against the same database.
