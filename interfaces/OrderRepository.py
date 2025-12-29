
from abc import ABC, abstractmethod
from domain.Order import Order


class OrderRepository(ABC):
    @abstractmethod
    def getById(self, orderId: str) -> Order:
        pass

    @abstractmethod
    def save(self, order: Order):
        pass