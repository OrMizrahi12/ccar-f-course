from datetime import date

from harborline import policy


def test_an_unknown_reason_is_refused_and_named():
    order_record = {
        "status": "delivered",
        "delivered_at": "2026-10-01T10:00:00Z",
        "promised_by": "2026-09-28",
        "shipping_fee": 6.95,
        "total": 56.95,
        "items": [{"sku": "SKU-1", "category": "home", "final_sale": False,
                   "unit_price": 50.0, "quantity": 1}],
    }
    decision = policy.check_refund(order_record, "lost_in_mail", sku="SKU-1")
    assert decision == {"allowed": False, "refund": 0, "rule": "unknown reason 'lost_in_mail'"}


def test_a_cancelled_order_refuses_a_change_of_mind_refund():
    order_record = {
        "status": "cancelled",
        "delivered_at": "2026-10-01T10:00:00Z",
        "promised_by": "2026-09-28",
        "shipping_fee": 6.95,
        "total": 56.95,
        "items": [{"sku": "SKU-1", "category": "home", "final_sale": False,
                   "unit_price": 50.0, "quantity": 1}],
    }
    decision = policy.check_refund(order_record, "changed_mind", sku="SKU-1", today=date(2026, 10, 16))
    assert decision == {"allowed": False, "refund": 0,
                        "rule": "this order was already cancelled or refunded"}


def test_a_sku_that_is_not_on_the_order_is_refused():
    order_record = {
        "status": "delivered",
        "delivered_at": "2026-10-01T10:00:00Z",
        "promised_by": "2026-09-28",
        "shipping_fee": 6.95,
        "total": 56.95,
        "items": [{"sku": "SKU-1", "category": "home", "final_sale": False,
                   "unit_price": 50.0, "quantity": 1}],
    }
    decision = policy.check_refund(order_record, "changed_mind", sku="SKU-9", today=date(2026, 10, 16))
    assert decision == {"allowed": False, "refund": 0, "rule": "item SKU-9 is not on this order"}


def test_a_damaged_item_reported_after_30_days_is_refused():
    order_record = {
        "status": "delivered",
        "delivered_at": "2026-09-01T10:00:00Z",
        "promised_by": "2026-08-28",
        "shipping_fee": 6.95,
        "total": 56.95,
        "items": [{"sku": "SKU-1", "category": "home", "final_sale": False,
                   "unit_price": 50.0, "quantity": 1}],
    }
    decision = policy.check_refund(order_record, "damaged", sku="SKU-1", today=date(2026, 10, 16))
    assert decision == {"allowed": False, "refund": 0,
                        "rule": "problems must be reported within 30 days of delivery"}


def test_a_delivery_exactly_5_days_late_gets_no_shipping_refund():
    order_record = {
        "status": "delivered",
        "delivered_at": "2026-10-03T10:00:00Z",
        "promised_by": "2026-09-28",
        "shipping_fee": 6.95,
        "total": 56.95,
        "items": [{"sku": "SKU-1", "category": "home", "final_sale": False,
                   "unit_price": 50.0, "quantity": 1}],
    }
    decision = policy.check_refund(order_record, "late_delivery")
    assert decision == {"allowed": False, "refund": 0,
                        "rule": "the order was not delivered more than 5 days late"}
