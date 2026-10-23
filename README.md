# Shop QA Tests

![qa](https://github.com/weronikategos/shop-qa-tests/actions/workflows/qa.yml/badge.svg)

Manual and automated tests for my online shop [flask-sql-shop](https://github.com/weronikategos/flask-sql-shop): a test plan, test cases, bug reports, API tests, end-to-end browser tests and SQL data integrity checks. Everything runs automatically in GitHub Actions.

## Application under test
A coffee and tea shop built with Flask: catalog, customer accounts, cart, checkout, a sales report and a REST API. Its code lives in a separate repository, [flask-sql-shop](https://github.com/weronikategos/flask-sql-shop).

## What's in this repository

| Folder / file | Contents |
|---|---|
| [`docs/test-plan.md`](docs/test-plan.md) | scope, techniques, environment, exit criteria, severity levels |
| [`docs/test-cases.md`](docs/test-cases.md) | 30+ test cases linked to the automated tests |
| [`docs/bugs/`](docs/bugs) | reports for the bugs I found |
| `tests/api/` | REST API tests (pytest + requests): contract, filters, 400/404 errors, response time |
| `tests/e2e/` | Playwright E2E tests: accounts, cart, checkout, stock limits |
| `tests/db/` | SQL queries checking data integrity in the database |
| `tests/test_known_bugs.py` | tests for the known bugs (marked `xfail`) |
| `postman/` | Postman collection, run in CI with newman |
| `.github/workflows/qa.yml` | starts the shop in Docker and runs every test on each push and once a day |

## Bugs found

| ID | Description | Severity |
|---|---|---|
| [BUG-001](docs/bugs/BUG-001.md) | every logged-in customer can see the sales report | high |
| [BUG-002](docs/bugs/BUG-002.md) | the server accepts an invalid email address | medium |

## Results
Latest run against the shop in Docker:

- **pytest:** 31 passed, 4 xfailed (the 4 expected failures are the tests for BUG-001 and BUG-002)
  - API: 14 tests, E2E (Playwright, Chromium): 11 tests, database (SQL): 6 tests
- **Postman / newman:** 7 requests, 16 assertions, 0 failures

The HTML report from each CI run can be downloaded from the run page in the Actions tab (artifact `test-report`).

## Tech stack
Python, pytest, Playwright, requests, Postman/newman, SQL (SQLite), Docker, GitHub Actions

## How to run locally
1. Start the shop (in the `flask-sql-shop` folder): `docker compose up -d`
2. In this folder:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v                                   # API and E2E tests
python -m pytest -m api                               # API only
python -m pytest tests/e2e --headed --slowmo 500      # E2E with a visible browser
```

The database tests need the path to a database file in `SHOP_DB` (they are skipped without it). To test a copy of the Docker database:

```bash
docker compose -f ../flask-sql-shop/docker-compose.yml cp shop:/app/instance/shop.db shop-copy.db
SHOP_DB=shop-copy.db python -m pytest -m db           # PowerShell: $env:SHOP_DB="shop-copy.db"; python -m pytest -m db
```

HTML report: `python -m pytest --html=report.html --self-contained-html`.

Postman: import `postman/shop-api.postman_collection.json` and `postman/local.postman_environment.json`, or run `npx newman run postman/shop-api.postman_collection.json -e postman/local.postman_environment.json`.
