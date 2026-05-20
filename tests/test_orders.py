import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orders import (  # noqa: E402
    InvalidOrderStatusError,
    OrderNotFoundError,
    OrderStore,
    STATUS_CANCELLED,
    STATUS_CONFIRMED,
    STATUS_PENDING,
)


class TestOrders(unittest.TestCase):
    def setUp(self):
        self.store = OrderStore()

    def test_calculate_sum(self):
        self.assertEqual(self.store.calculate_order_sum([10, 5, 5]), 20)

    def test_calculate_sum_empty(self):
        with self.assertRaises(ValueError):
            self.store.calculate_order_sum([])

    def test_calculate_sum_negative(self):
        with self.assertRaises(ValueError):
            self.store.calculate_order_sum([10, -1])

    def test_create_order(self):
        order = self.store.create_order(customer_id=1, prices=[100, 50])

        self.assertEqual(order["customer_id"], 1)
        self.assertEqual(order["status"], STATUS_PENDING)
        self.assertEqual(order["price"], 150)

    def test_create_order_has_id(self):
        order = self.store.create_order(customer_id=2, prices=[10])

        self.assertEqual(order["id"], 1)

    def test_change_status(self):
        order = self.store.create_order(customer_id=1, prices=[10])
        updated = self.store.change_order_status(order["id"], STATUS_CONFIRMED)

        self.assertEqual(updated["status"], STATUS_CONFIRMED)

    def test_change_status_not_found(self):
        with self.assertRaises(OrderNotFoundError):
            self.store.change_order_status(999, STATUS_CONFIRMED)

    def test_change_status_cancelled(self):
        order = self.store.create_order(customer_id=1, prices=[10])
        self.store.cancel_order(order["id"])

        with self.assertRaises(InvalidOrderStatusError):
            self.store.change_order_status(order["id"], STATUS_CONFIRMED)

    def test_cancel_order(self):
        order = self.store.create_order(customer_id=1, prices=[10])
        cancelled = self.store.cancel_order(order["id"])

        self.assertEqual(cancelled["status"], STATUS_CANCELLED)

    def test_cancel_order_twice(self):
        order = self.store.create_order(customer_id=1, prices=[10])
        self.store.cancel_order(order["id"])

        with self.assertRaises(InvalidOrderStatusError):
            self.store.cancel_order(order["id"])


if __name__ == "__main__":
    unittest.main()
