
from interfaces.OrderRepository import OrderRepository
from interfaces.PaymentGateway import PaymentGateway
from .PaymentResult import PaymentResult


class PayOrderUseCase:
    def __init__(self, orderRepository: OrderRepository, paymentGateway: PaymentGateway):
        self.orderRepository = orderRepository
        self.paymentGateway = paymentGateway
    
    def execute(self, orderId: str) -> PaymentResult:
        try:
            order = self.orderRepository.getById(orderId)
            if order is None:
                return PaymentResult(False, "Order not found", orderId)
            order.pay()
            paymentSuccess = self.paymentGateway.charge(orderId, order.getTotalAmount())
            if not paymentSuccess:
                return PaymentResult(False, "Payment failed", orderId)
            self.orderRepository.save(order)
            return PaymentResult(True, "Payment successful", orderId)
        except Exception as e:
            return PaymentResult(False, str(e), orderId)
