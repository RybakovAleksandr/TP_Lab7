import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from domain.Order import Order
from domain.OrderLine import OrderLine
from domain.Money import Money
from domain.OrderStatus import OrderStatus
from application.PayOrderUseCase import PayOrderUseCase
from application.PaymentResult import PaymentResult
from infrastructure.InMemoryOrderRepository import InMemoryOrderRepository
from infrastructure.FakePaymentGateway import FakePaymentGateway
import uuid


class TestPayOrderUseCase:
    @pytest.fixture
    def setup(self):
        self.order_repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.order_repository, self.payment_gateway)
        
        # Создаем тестовый заказ
        order_id = str(uuid.uuid4())
        lines = []
        
        self.test_order = Order(
            id=order_id,
            lines=lines,
            status=OrderStatus.PENDING
        )
        
        # Добавляем товары
        self.test_order.addLine(OrderLine(
            productId="prod1",
            productName="Product 1",
            price=Money(1000, "USD"),
            quantity=2
        ))
        self.test_order.addLine(OrderLine(
            productId="prod2",
            productName="Product 2",
            price=Money(500, "USD"),
            quantity=1
        ))
        
        self.order_repository.save(self.test_order)
        yield
        self.order_repository.clear()

    def test_successful_payment(self, setup):
        result = self.use_case.execute(self.test_order.getId())
        
        assert result.success is True
        assert result.message == "Payment successful"
        assert result.orderId == self.test_order.getId()
        
        paid_order = self.order_repository.getById(self.test_order.getId())
        assert paid_order.getStatus() == OrderStatus.PAID

    def test_payment_empty_order(self, setup):
        # Создаем пустой заказ
        empty_order_id = str(uuid.uuid4())
        empty_order = Order(
            id=empty_order_id,
            lines=[],
            status=OrderStatus.PENDING
        )
        self.order_repository.save(empty_order)
        
        result = self.use_case.execute(empty_order.getId())
        
        # Тест должен ожидать, что оплата пустого заказа вернет False
        # и сообщение об ошибке
        assert result.success is False
        # Проверяем, что в результате есть сообщение об ошибке
        assert result.message  # Просто проверяем, что сообщение есть

    def test_double_payment_error(self, setup):
        # Первая оплата
        self.use_case.execute(self.test_order.getId())
        
        # Вторая попытка оплаты
        result = self.use_case.execute(self.test_order.getId())
        
        assert result.success is False
        assert "already paid" in result.message.lower()

    def test_cannot_modify_order_after_payment(self, setup):
        # Оплачиваем заказ
        self.use_case.execute(self.test_order.getId())
        paid_order = self.order_repository.getById(self.test_order.getId())
        
        # Пытаемся добавить товар в оплаченный заказ
        new_line = OrderLine(
            productId="prod3",
            productName="Product 3",
            price=Money(300, "USD"),
            quantity=1
        )
        
        # Должно вызывать исключение при попытке изменить оплаченный заказ
        with pytest.raises(Exception) as exc_info:
            paid_order.addLine(new_line)
        
        assert "Cannot change paid order" in str(exc_info.value)

    def test_total_amount_calculation(self, setup):
        total = self.test_order.getTotalAmount()

        assert total.getAmount() == 2500
        assert total.getCurrency() == "USD"

    def test_payment_gateway_failure(self, setup):
        # Настраиваем платежный шлюз на неудачу для этого заказа
        self.payment_gateway.setAlwaysSucceed(False)
        self.payment_gateway.addFailedOrder(self.test_order.getId())
        
        result = self.use_case.execute(self.test_order.getId())

        # PayOrderUseCase должен вернуть success=False при неудачном платеже
        assert result.success is False
        assert result.message == "Payment failed"

    def test_order_not_found(self, setup):
        # Используем try-except для обработки возможного исключения
        try:
            result = self.use_case.execute("non-existent-id")
            # Если код дошел сюда, проверяем результат
            assert result.success is False
            assert "Order not found" in result.message
        except Exception as e:
            # Если возникает исключение, тест должен падать
            pytest.fail(f"Unexpected exception: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])