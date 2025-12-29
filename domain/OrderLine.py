from .Money import Money


class OrderLine:
    def __init__(self, productId: str, productName: str, price: Money, quantity: int):
        self.productId = productId
        self.productName = productName
        self.price = price
        self.quantity = quantity
    
    def getProductId(self) -> str:
        return self.productId
    
    def getProductName(self) -> str:
        return self.productName
    
    def getPrice(self) -> Money:
        return self.price
    
    def getQuantity(self) -> int:
        return self.quantity
    
    def getTotal(self) -> Money:
        return Money(self.price.getAmount() * self.quantity, self.price.getCurrency())
    
    
    
