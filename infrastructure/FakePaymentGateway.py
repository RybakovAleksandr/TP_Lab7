
from interfaces.PaymentGateway import PaymentGateway
from domain.Money import Money


class FakePaymentGateway(PaymentGateway):
    def __init__(self):
        self.failedOrders = set()
        self.alwaysSucceed = True

    def setAlwaysSucceed(self, alwaysSucceed: bool):
        self.alwaysSucceed = alwaysSucceed

    def addFailedOrder(self, orderId: str):
        self.failedOrders.add(orderId)

    def charge(self, orderId: str, amount: Money) -> bool:
        if not self.alwaysSucceed and orderId in self.failedOrders:
            return False
        print(f"Processing payment for order {orderId}: {amount}")
        return True

