from entities.transaction import Transaction

class User:
    def __init__(self, username: str, password: str, is_admin: bool = False):
        self.username = username
        self.password = password
        self.balance = 0
        self.transactions = []  # 交易列表
        self.is_admin = is_admin  # 是否管理员

    def update_password(self, new_password: str):
        self.password = new_password

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def to_dict(self):
        """将 User 对象转换为字典"""
        return {
            "username": self.username,
            "password": self.password,
            "balance": self.balance,
            "is_admin": self.is_admin,
            "transactions": [t.to_dict() for t in self.transactions],  # 确保序列化 Transaction 对象
        }

    @staticmethod
    def from_dict(data):
        """从字典恢复 User 对象"""
        user = User(
            username=data["username"],
            password=data["password"],
            is_admin=data.get("is_admin", False),
        )
        user.balance = data["balance"]
        return user
