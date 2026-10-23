import pytest

pytestmark = pytest.mark.api

REQUIRED_FIELDS = {"product_id": int, "name": str, "description": str, "price": float,
                   "stock": int, "category_id": int, "category": str}


@pytest.fixture
def products(api):
    response = api.get(f"{api.base_url}/api/products")
    assert response.status_code == 200
    return response.json()


def test_products_list_is_not_empty(products):
    """TC-API-03"""
    assert len(products) > 0


def test_products_have_required_fields_and_types(products):
    """TC-API-04: API contract, every field has the expected type"""
    for product in products:
        for field, expected_type in REQUIRED_FIELDS.items():
            assert field in product, f"field {field} missing in product {product.get('product_id')}"
            value = product[field]
            if expected_type is float:
                assert isinstance(value, (int, float))
            else:
                assert isinstance(value, expected_type), f"{field}={value!r}"


def test_prices_positive_and_stock_not_negative(products):
    """TC-API-05"""
    assert all(p["price"] > 0 for p in products)
    assert all(p["stock"] >= 0 for p in products)


def test_product_ids_are_unique(products):
    """TC-API-06"""
    ids = [p["product_id"] for p in products]
    assert len(ids) == len(set(ids))


def test_filter_by_category_returns_only_that_category(api):
    """TC-API-07"""
    categories = api.get(f"{api.base_url}/api/categories").json()
    for category in categories:
        filtered = api.get(f"{api.base_url}/api/products", params={"category": category["category_id"]}).json()
        assert filtered, f"category {category['name']} is empty"
        assert {p["category"] for p in filtered} == {category["name"]}


def test_filter_with_unknown_category_returns_empty_list(api):
    """TC-API-08: boundary value, a category that doesn't exist"""
    response = api.get(f"{api.base_url}/api/products", params={"category": 99999})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("bad_value", ["abc", "-1", "1.5", ""])
def test_filter_with_invalid_category_returns_400(api, bad_value):
    """TC-API-09: invalid input"""
    response = api.get(f"{api.base_url}/api/products", params={"category": bad_value})
    assert response.status_code == 400
    assert "error" in response.json()


def test_single_product_matches_list(api, products):
    """TC-API-10"""
    first = products[0]
    response = api.get(f"{api.base_url}/api/products/{first['product_id']}")
    assert response.status_code == 200
    assert response.json() == first


def test_missing_product_returns_404_json(api):
    """TC-API-11"""
    response = api.get(f"{api.base_url}/api/products/999999")
    assert response.status_code == 404
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.json() == {"error": "Not found"}
