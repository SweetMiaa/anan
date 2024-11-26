from datetime import datetime
class Transaction:
    def __init__(self, from_user: str, to_user: str, amount: int, description: str = ""):
        self.from_user = from_user
        self.to_user = to_user
        self.amount = amount
        self.description = description

    def to_dict(self):
        """将 Transaction 对象转换为字典"""
        return {
            "from_user": self.from_user,
            "to_user": self.to_user,
            "amount": self.amount,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data):
        transaction = Transaction(
            from_user=data["from_user"],
            to_user=data["to_user"],
            amount=data["amount"],
            description=data["description"],
        )
        return transaction
