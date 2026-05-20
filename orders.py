STATUS_PENDING = "pending"
STATUS_CONFIRMED = "confirmed"
STATUS_CANCELLED = "cancelled"


class OrderNotFoundError(Exception):
    pass


class InvalidOrderStatusError(Exception):
    pass


class OrderStore:
    def __init__(self):
        self._orders = {}
        self._next_id = 1

    def calculate_order_sum(self, prices):
        if not prices:
            raise ValueError("Order must contain at least one price")
        if any(price < 0 for price in prices):
            raise ValueError("Prices cannot be negative")
        return sum(prices)

    def create_order(self, customer_id, prices):
        order = {
            "id": self._next_id,
            "customer_id": customer_id,
            "status": STATUS_PENDING,
            "price": self.calculate_order_sum(prices),
        }
        self._orders[self._next_id] = order
        self._next_id += 1
        return order.copy()

    def change_order_status(self, order_id, status):
        order = self._get_order(order_id)
        if order["status"] == STATUS_CANCELLED:
            raise InvalidOrderStatusError("Cannot change status of a cancelled order")
        order["status"] = status
        return order.copy()

    def cancel_order(self, order_id):
        order = self._get_order(order_id)
        if order["status"] == STATUS_CANCELLED:
            raise InvalidOrderStatusError("Order is already cancelled")
        order["status"] = STATUS_CANCELLED
        return order.copy()

    def _get_order(self, order_id):
        order = self._orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")
        return order
