class Money:
    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency
    
    def getAmount(self) -> int:
        return self.amount
    
    def getCurrency(self) -> str:
        return self.currency
    
    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise Exception("Different currencies")
        return Money(self.amount + other.amount, self.currency)
    

    