class PaymentResult:
    def __init__(self, success: bool, message: str, orderId: str):
        self.success = success
        self.message = message
        self.orderId = orderId
    
    def isSuccess(self) -> bool:
        return self.success

    def getMessage(self) -> str:
        return self.message

    def getOrderId(self) -> str:
        return self.orderId
    
        