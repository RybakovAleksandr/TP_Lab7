
from .OrderStatus import OrderStatus
from .Money import Money
from .OrderLine import OrderLine


class Order:
    def __init__(self, id: str, lines: list[OrderLine], status: OrderStatus):
        self.id = id
        self.lines = lines
        self.status = status
        self.totalAmount = self.calculateTotal()
    
    def getId(self) -> str:
        return self.id
    
    def getLines(self) -> list[OrderLine]:
        return self.lines()
    
    def getStatus(self) -> OrderStatus:
        return self.status
    
    def getTotalAmount(self) -> Money:
        return self.totalAmount
    
    def calculateTotal(self) -> Money:
        total = Money(0, "USD")
        for line in self.lines:
            total = total.add(line.getTotal())
        return total
    
    def addLine(self, line: OrderLine):
        if self.status == OrderStatus.PAID:
            raise Exception("Cannot change paid order")
        self.lines.append(line)
        self.totalAmount = self.calculateTotal()
    
    def removeLine(self, productId: str):
        if self.status == OrderStatus.PAID:
            raise Exception("Cannot change paid order")
        self.lines = [line for line in self.lines if line.productId != productId]
        self.totalAmount = self.calculateTotal()

    def pay(self):
        if len(self.lines) == 0:
            raise Exception("Cannot pay empty order")
        if self.status == OrderStatus.PAID:
            raise Exception("Order is already paid")
        self.status = OrderStatus.PAID



