"""Data integrity checks run as SQL queries directly on the shop database (read-only)."""
import pytest

pytestmark = pytest.mark.db


def count(db, sql):
    return db.execute(sql).fetchone()[0]


def test_no_negative_stock(db):
    """TC-DB-01"""
    assert count(db, "SELECT COUNT(*) FROM products WHERE stock < 0") == 0


def test_order_total_equals_sum_of_items(db):
    """TC-DB-02: order total matches its items (1 grosz tolerance)"""
    sql = """SELECT o.order_id, o.total, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS items_total
             FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
             GROUP BY o.order_id
             HAVING ABS(o.total - items_total) > 0.01"""
    assert db.execute(sql).fetchall() == []


def test_every_order_has_items(db):
    """TC-DB-03: no empty orders"""
    sql = """SELECT COUNT(*) FROM orders o
             LEFT JOIN order_items oi ON oi.order_id = o.order_id
             WHERE oi.order_id IS NULL"""
    assert count(db, sql) == 0


def test_no_orphan_rows(db):
    """TC-DB-04: every order item points to an existing order and product"""
    assert count(db, """SELECT COUNT(*) FROM order_items oi
                        LEFT JOIN orders o ON o.order_id = oi.order_id
                        WHERE o.order_id IS NULL""") == 0
    assert count(db, """SELECT COUNT(*) FROM order_items oi
                        LEFT JOIN products p ON p.product_id = oi.product_id
                        WHERE p.product_id IS NULL""") == 0


def test_emails_unique_case_insensitive(db):
    """TC-DB-05"""
    assert count(db, """SELECT COUNT(*) FROM (SELECT LOWER(email) FROM customers
                        GROUP BY LOWER(email) HAVING COUNT(*) > 1)""") == 0


def test_passwords_are_hashed(db):
    """TC-DB-06: no plain-text passwords in the database"""
    assert count(db, """SELECT COUNT(*) FROM customers
                        WHERE password_hash NOT LIKE 'scrypt:%' AND password_hash NOT LIKE 'pbkdf2:%'""") == 0
