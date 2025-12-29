
from abc import ABC, abstractmethod
from domain.Money import Money


def PaymentGateway(ABC):
    @abstractmethod
    def charge(self, orderId: str, amount: Money) -> bool:
        pass


