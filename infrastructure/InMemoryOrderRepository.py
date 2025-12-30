
from typing import Dict
from interfaces.OrderRepository import OrderRepository
from domain.Order import Order


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders: Dict[str, Order] = {}
    
    def getById(self, orderId: str) -> Order:
        return self.orders[orderId]
    
    def save(self, order: Order):
        self.orders[order.getId()] = order

    def clear(self):
        self.orders.clear()